# Copyright (c) 2016 Civic Knowledge. This file is licensed under the terms of the
# Revised BSD License, included in this distribution as LICENSE

"""
Generate rows from a variety of paths, references or other input
"""
import collections
import csv
import logging
import pathlib
from collections import OrderedDict
from collections.abc import MutableSequence
from itertools import groupby
from os.path import dirname, getmtime
from time import time

from metatab import DEFAULT_METATAB_FILE
from metatab.exc import MetatabError, FormatError
from metatab.parser import TermParser
from metatab.resolver import WebResolver
from metatab.util import slugify, get_cache
from rowgenerators import parse_app_url
from rowgenerators.exceptions import SourceError, AppUrlError

from .terms import SectionTerm, RootSectionTerm, Term
from .util import import_name_or_class

logger = logging.getLogger('doc')
debug_logger = logging.getLogger('debug')


class MetatabDoc(object):

    def __init__(self, ref=None, decl=None, package_url=None, cache=None, resolver=None, clean_cache=False):

        self._input_ref = ref

        self._cache = cache if cache else get_cache()

        self.decl_terms = {}
        self.decl_sections = {}

        self.terms = []
        self.sections = OrderedDict()
        self.super_terms = {}
        self.derived_terms = {}
        self.errors = []
        self.package_url = package_url

        self.resolver = resolver or WebResolver()

        if decl is None:
            self.decls = []
        elif not isinstance(decl, MutableSequence):
            self.decls = [decl]
        else:
            self.decls = decl

        self.root = RootSectionTerm(doc=self)
        self.add_section(self.root)

        self.load_declarations(self.decls)

        if ref:
            try:
                self._ref = parse_app_url(ref)

                if self._ref.scheme == 'file':
                    try:
                        self._mtime = getmtime(self._ref.path)
                    except (FileNotFoundError, OSError):
                        self._mtime = 0
                else:
                    self._mtime = 0

            except AppUrlError as e:  # ref is probably a generator, not a string or Url
                self._ref = None

            self._term_parser = TermParser(ref, resolver=self.resolver, doc=self)

            try:
                self.load_terms(self._term_parser)
            except SourceError as e:
                raise MetatabError("Failed to load terms for document '{}': {}".format(self._ref, e))


        else:
            self._ref = None
            self._term_parser = None
            self._mtime = time()

    @property
    def ref(self):
        return self._ref

    @property
    def path(self):
        """Return the path to the file, if the ref is a file"""

        if not isinstance(self.ref, str):
            return None

        u = parse_app_url(self.ref)

        if u.inner.proto != 'file':
            return None

        return u.path

    @property
    def cache(self):
        """Return the file cache used by this document"""
        return self._cache

    @property
    def mtime(self):
        return self._mtime

    def as_version(self, ver):
        """Return an edited name, with a different version number or no version

        :param ver: A Version number for the returned document. May also be an integer prefixed with '+'
        ( '+1' ) to set the version ahead of this document's version. Prefix with a '-' to set a version behind.

        Typical use of the version math feature is to get the name of a document one version behind:

        >>> doc.as_version('-1')

        """

        return self._generate_identity_name(ver)

    @property
    def doc_dir(self):
        """The absolute directory of the document"""
        from os.path import abspath

        if not self.ref:
            return None

        u = parse_app_url(self.ref)
        return abspath(dirname(u.path))

    @classmethod
    def register_term_class(cls, term_name, class_or_name):
        """
        Convinence function for TermParser.register_term_class(), which registers a Term subclass for use with a
        term name

        :param term_name: A fully qualified term name.
        :param class_or_name: A class, or a fully-qualified, dotted class name.
        :return:
        """

        return TermParser.register_term_class(term_name, class_or_name)

    def load_declarations(self, decls):

        if not decls:
            return

        extant_decls = [t.value for t in self.find('Root.Declare')]

        rg = self.resolver.get_row_generator([['Declare', dcl] for dcl in decls if dcl not in extant_decls],
                                             cache=self._cache)

        term_interp = TermParser(rg, resolver=self.resolver, doc=self)

        list(term_interp)

        dd = term_interp.declare_dict

        self.decl_terms.update(dd['terms'])
        self.decl_sections.update(dd['sections'])

        return self

    def add_term(self, t, add_section=True):
        t.doc = self

        if t in self.terms:
            return

        assert t.section or t.join_lc == 'root.root', t

        # Section terms don't show up in the document as terms
        if isinstance(t, SectionTerm):
            self.add_section(t)
        else:
            self.terms.append(t)

        if add_section and t.section and t.parent_term_lc == 'root':
            t.section = self.add_section(t.section)
            t.section.add_term(t)

        if not t.child_property_type or t.child_property_type == 'any':
            t.child_property_type = self.decl_terms \
                .get(t.join, {}) \
                .get('childpropertytype', 'any')

        if not t.term_value_name or t.term_value_name == t.section.default_term_value_name:
            t.term_value_name = self.decl_terms \
                .get(t.join, {}) \
                .get('termvaluename', t.section.default_term_value_name)

        assert t.section or t.join_lc == 'root.root', t

    def get_term_class(self, term_name):

        tnl = term_name.lower()

        try:
            return import_name_or_class(TermParser.term_classes[tnl])
        except KeyError:
            pass

        try:
            return import_name_or_class(TermParser.term_classes[self.super_terms[tnl]])
        except KeyError:
            pass

        return Term

    def remove_term(self, t):
        """Only removes top-level terms. Child terms can be removed at the parent. """

        try:
            self.terms.remove(t)
        except ValueError:
            pass

        if t.section and t.parent_term_lc == 'root':
            t.section = self.add_section(t.section)
            t.section.remove_term(t, remove_from_doc=False)

        if t.parent:
            try:
                t.parent.remove_child(t)

            except ValueError:
                pass

    def add_section(self, s):

        s.doc = self

        assert isinstance(s, SectionTerm), str(s)

        # Coalesce sections, and if a foreign term is added with a foreign section
        # it will get re-assigned to the local section
        if s.value.lower() not in self.sections:
            self.sections[s.value.lower()] = s

        return self.sections[s.value.lower()]

    def section_args(self, section_name):
        """Return section arguments for the named section, if it is defined"""
        return self.decl_sections.get(section_name.lower(), {}).get('args', [])

    def new_section(self, name, params=None):
        """Return a new section"""
        self.sections[name.lower()] = SectionTerm(None, name, term_args=params, doc=self)

        # Set the default arguments
        s = self.sections[name.lower()]

        if name.lower() in self.decl_sections:
            s.args = self.decl_sections[name.lower()]['args']

        return s

    def get_or_new_section(self, name, params=None):
        """Create a new section or return an existing one of the same name"""
        if name not in self.sections:
            self.sections[name.lower()] = SectionTerm(None, name, term_args=params, doc=self)

        return self.sections[name.lower()]

    def get_section(self, name, default=False):
        try:
            return self.sections[name.lower()]
        except KeyError:
            if default is False:
                raise KeyError("No section for '{}'; sections are: '{}' ".format(name.lower(), self.sections.keys()))
            else:
                return default

    def sort_sections(self, order):
        """
        Sort sections according to the section names in the order list. All remaining sections
         are added to the end in their original order

        :param order: Iterable of section names
        :return:
        """

        order_lc = [e.lower() for e in order]

        sections = OrderedDict((k, self.sections[k]) for k in order_lc if k in self.sections)

        sections.update((k, self.sections[k]) for k in self.sections.keys() if k not in order_lc)

        assert len(self.sections) == len(sections)

        self.sections = sections

    def __getitem__(self, item):
        """Dereference a section name"""

        # Handle dereferencing a list of sections
        if isinstance(item, collections.abc.Iterable) and not isinstance(item, str):
            return [self.__getitem__(e) for e in item]

        else:
            return self.get_section(item)

    def __delitem__(self, item):

        try:
            if item in self.sections:
                for t in self.sections[item]:
                    self.terms.remove(t)

            del self.sections[item.lower()]
        except KeyError:
            # Ignore errors
            pass

    def __contains__(self, item):

        return item.lower() in self.sections

    def __iter__(self):
        """Iterate over sections"""
        for s in self.sections.values():
            yield s

    def find(self, term, value=False, section=None, _expand_derived=True, **kwargs):
        """Return a list of terms, possibly in a particular section. Use joined term notation, such as 'Root.Name' The kwargs arg is used to set term properties, all of which match returned terms, so ``name='foobar'`` will match terms that have a ``name`` property of ``foobar``

        :param term: The type of term to find, in fully-qulified notation, or use '*' for wild cards in either the parent or the record parts, such as 'Root.*', '*.Table' or '*.*'
        :param value: Select terms with a given value
        :param section: The name of the section in which to restrict the search
        :param kwargs:  See additional properties on which to match terms.

        """

        import itertools

        if kwargs:  # Look for terms with particular property values

            terms = self.find(term, value, section)

            found_terms = []

            for t in terms:
                if all(t.get_value(k) == v for k, v in kwargs.items()):
                    found_terms.append(t)

            return found_terms

        def in_section(term, section):

            if section is None:
                return True

            if term.section is None:
                return False

            if isinstance(section, (list, tuple)):
                return any(in_section(t, e) for e in section)
            else:
                return section.lower() == term.section.name.lower()

        # Try to replace the term with the list of its derived terms; that is, replace the super-class with all
        # of the derived classes, but only do this expansion once.
        if _expand_derived:
            try:
                try:
                    # Term is a string
                    term = list(self.derived_terms[term.lower()]) + [term]
                except AttributeError:  # Term is hopefully a list
                    terms = []
                    for t in term:
                        terms.append(term)
                        for dt in self.derived_terms[t.lower()]:
                            terms.append(dt)
            except KeyError as e:
                pass

        # Find any of a list of terms
        if isinstance(term, (list, tuple)):
            return list(
                itertools.chain(*[self.find(e, value=value, section=section, _expand_derived=False) for e in term]))

        else:

            term = term.lower()

            found = []

            if not '.' in term:
                term = 'root.' + term

            if term.startswith('root.'):
                term_gen = self.terms  # Just the root level terms
            else:
                term_gen = self.all_terms  # All terms, root level and children.

            for t in term_gen:

                if t.join_lc == 'root.root':
                    continue

                assert t.section or t.join_lc == 'root.root' or t.join_lc == 'root.section', t

                if (t.term_is(term)
                        and in_section(t, section)
                        and (value is False or value == t.value)):
                    found.append(t)

            return found

    def find_first(self, term, value=False, section=None, **kwargs):

        terms = self.find(term, value=value, section=section, **kwargs)

        if len(terms) > 0:
            return terms[0]
        else:
            return None

    def find_first_value(self, term, value=False, section=None, **kwargs):

        term = self.find_first(term, value=value, section=section, **kwargs)

        if term is None:
            return None
        else:
            return term.value

    def get(self, term, default=None):
        """Return the first term, returning the default if no term is found"""
        v = self.find_first(term)

        if not v:
            return default
        else:
            return v

    def get_value(self, term, default=None, section=None):
        """Return the first value, returning the default if no term is found"""
        term = self.find_first(term, value=False, section=section)

        if term is None:
            return default
        else:
            return term.value

    def resolve_url(self, url):
        """Resolve an application specific URL to a web URL"""
        return url

    def load_terms(self, terms):
        """Create a builder from a sequence of terms, usually a TermInterpreter"""

        # if self.root and len(self.root.children) > 0:
        #    raise MetatabError("Can't run after adding terms to document.")

        for t in terms:

            t.doc = self

            if t.term_is('root.root'):
                if not self.root:
                    self.root = t
                    self.add_section(t)

                continue

            if t.term_is('root.section'):
                self.add_section(t)

            elif t.parent_term_lc == 'root':
                self.add_term(t)

            else:
                # These terms aren't added to the doc because they are attached to a
                # parent term that is added to the doc.
                assert t.parent is not None

        try:
            dd = terms.declare_dict

            self.decl_terms.update(dd['terms'])
            self.decl_sections.update(dd['sections'])

            self.super_terms.update(terms.super_terms())

            kf = lambda e: e[1]  # Sort on the value
            self.derived_terms = {k: set(e[0] for e in g)
                                  for k, g in groupby(sorted(self.super_terms.items(), key=kf), kf)}

        except AttributeError as e:
            pass

        try:
            self.errors = terms.errors_as_dict()
        except AttributeError:
            self.errors = {}

        return self

    def load_rows(self, row_generator):

        term_interp = TermParser(self, row_generator)

        return self.load_terms(term_interp)

    def cleanse(self):
        """Clean up some terms, like ensuring that the name is a slug"""
        from .util import slugify

        self.ensure_identifier()

        try:
            self.update_name()
        except MetatabError:

            identifier = self['Root'].find_first('Root.Identifier')

            name = self['Root'].find_first('Root.Name')

            if name and name.value:
                name.value = slugify(name.value)
            elif name:
                name.value = slugify(identifier.value)
            else:
                self['Root'].get_or_new_term('Root.Name').value = slugify(identifier.value)

    def clean_unused_schema_terms(self):

        # Remove unused columns in the schema, and add new ones
        schema_section = self.get_section('Schema')

        if schema_section:
            used_args = set()
            section_args = [e.lower() for e in schema_section.args]

            for table in schema_section.find('Root.Table'):
                for column in table.find('Table.Column'):
                    for k, v in column.props.items():
                        if v and v.strip():
                            used_args.add(k)

            for arg in set(section_args) - used_args:
                try:
                    print("Removing ", arg.title())
                    schema_section.remove_arg(arg.title())
                except ValueError as e:
                    pass

            for arg in used_args - set(section_args):
                schema_section.add_arg(arg)

            # Remove any empty properties
            for t in schema_section.find('Root.Table'):
                for c in t.find('Table.Column'):
                    for child in list(c.children):
                        if not child.value or not child.value.strip():
                            c.remove_child(child)

    def ensure_identifier(self):
        from uuid import uuid4

        identifier = self.find_first('Root.Identifier', section='Root')

        if not identifier:
            identifier = self['Root'].new_term('Root.Identifier', None)

        if not identifier.value:
            identifier.value = str(uuid4())

        assert identifier is not None and bool(identifier.value)

    def _has_semver(self):

        version = self['Root'].find_first('Root.Version')

        if not version:
            return False

        return any([
            version.find_first('Version.Major'),
            version.find_first('Version.Minor'),
            version.find_first('Version.Patch')
        ])

    def update_version(self):

        version = self['Root'].find_first('Root.Version')

        if not version:
            return None

        major = version.find_first('Version.Major')
        minor = version.find_first('Version.Minor')
        patch = version.find_first('Version.Patch')

        # If none are defined, this isn't a semantic version
        # so just return the Version value.
        if not any([major, minor, patch]):
            return version.value

        # if one of the exists, they all have to exist,
        # and this is a semantic version
        for term, term_name in ((major, 'Version.Major'),
                                (minor, 'Version.Minor'),
                                (patch, 'Version.Patch')):

            if not term:
                term = version.new_child(term_name, 1)

            if term.value is None:
                term.value = 0

        major = version.find_first('Version.Major')
        minor = version.find_first('Version.Minor')
        patch = version.find_first('Version.Patch')

        assert all([major, minor, patch])

        templ = '{}.{}.{}'
        values = (major.value, minor.value, patch.value)

        version.value = templ.format(*values)

        build = version.find_first('Version.Build')
        if build:
            templ += '.{}'
            values = values + (build.value,)

        version.value = templ.format(*values)

        return version.value

    def update_name(self, force=False, create_term=False, report_unchanged=True, mod_version=False):
        """Generate the Root.Name term from DatasetName, Version, Origin, TIme and Space"""

        updates = []

        self.ensure_identifier()

        name_term = self.find_first('Root.Name')

        if not name_term:
            if create_term:
                name_term = self['Root'].new_term('Root.Name', '')
            else:
                updates.append("No Root.Name, can't update name")
                return updates

        orig_name = name_term.value

        identifier = self.get_value('Root.Identifier')

        datasetname = self.get_value('Root.Dataset')

        if datasetname:

            name = self._generate_identity_name(mod_version=mod_version)

            if name != orig_name or force:
                name_term.value = name
                updates.append("Changed Name")
            else:
                if report_unchanged:
                    updates.append("Name did not change")

        elif not orig_name:

            if not identifier:
                updates.append("Failed to find DatasetName term or Identity term. Giving up")

            else:
                updates.append("Setting the name to the identifier")
                name_term.value = identifier

        elif orig_name == identifier:
            if report_unchanged:
                updates.append("Name did not change")

        else:
            # There is no DatasetName, so we can't gneerate name, and the Root.Name is not empty, so we should
            # not set it to the identity.
            updates.append("No Root.Dataset, so can't update the name")

        return updates

    def _generate_identity_name(self, mod_version=False):

        """mod_version == False -> dpn't change the version
           mod_version == None -> remove the version
           mod_version == Something else -> change the versino to somethig else"""

        datasetname = self.find_first_value('Root.Dataset', section='Root')
        origin = self.find_first_value('Root.Origin', section='Root')
        time = self.find_first_value('Root.Time', section='Root')
        space = self.find_first_value('Root.Space', section='Root')
        grain = self.find_first_value('Root.Grain', section='Root')
        variant = self.find_first_value('Root.Variant', section='Root')

        self.update_version()

        if self._has_semver():
            # Modifyable part is the patch
            mv = self['Root'].get_value('Version.Patch')

            def set_ver(mv):
                self['Root'].find_first('Version.Patch').value = mv

        else:
            # Modifyable part is the whole version
            mv = self['Root'].get_value('Version')

            def set_ver(mv):
                self['Root'].find_first('Version').value = mv


        if mod_version is False:
            # Don't change the version
            pass
        elif mod_version is None:
            # Set the version to nothing -- the nonver name
            mv = None

        elif str(mod_version)[0] == '+' or str(mod_version)[0] == '-':

            # Increment or decrement the version

            try:
                int(mv)
            except ValueError:
                raise MetatabError(
                    "When specifying version math, version value in Root.Version or Version.Patch  term must be an integer")

            # Excel likes to make integers into floats
            try:
                if int(mv) == float(mv):
                    mv = int(mv)

            except (ValueError, TypeError):
                pass

            if mod_version[0] == '+':
                mv = str(int(mv) + int(mod_version[1:] if mod_version[1:] else 1))
            else:
                mv = str(int(mv) - int(mod_version[1:] if mod_version[1:] else 1))

        else:
            # Set the version to a specific string
            mv = mod_version

        if mv is None:
            version = None
        else:
            set_ver(mv)
            version = self.update_version()

        parts = [slugify(str(e).replace('-', '_')) for e in (
            origin, datasetname, time, space, grain, variant, version)
                 if e and str(e).strip()]

        return '-'.join(parts)

    def as_dict(self, replace_value_names=True):
        """Iterate, link terms and convert to a dict"""

        # This function is a hack, due to confusion between the root of the document, which
        # should contain all terms, and the root section, which has only terms that are not
        # in another section. So, here we are taking the Root section, and adding all of the other
        # terms to it, as if it were also the root of the document tree.

        r = RootSectionTerm(doc=self)

        for s in self:  # Iterate over sections
            for t in s:  # Iterate over the terms in each section.
                r.terms.append(t)

        return r.as_dict(replace_value_names)

    @property
    def rows(self):
        """Iterate over all of the rows"""

        for s_name, s in self.sections.items():

            # Yield the section header
            if s.name != 'Root':
                yield ['']  # Unecessary, but makes for nice formatting. Should actually be done just before write
                yield ['Section', s.value] + s.property_names

            # Yield all of the rows for terms in the section
            for row in s.rows:
                term, value = row

                term = term.replace('root.', '').title()

                try:
                    yield [term] + value
                except:
                    yield [term] + [value]

    @property
    def lines(self):
        """Iterate over all of the rows as text lines"""

        for s_name, s in self.sections.items():
            yield from s.lines

    @property
    def all_terms(self):
        """Iterate over all of the terms. The self.terms property has only root level terms. This iterator
        iterates over all terms"""

        for s_name, s in self.sections.items():

            # Yield the section header
            if s.name != 'Root':
                yield s

            # Yield all of the rows for terms in the section
            for rterm in s:
                yield rterm
                for d in rterm.descendents:
                    yield d

    def as_csv(self):
        """Return a CSV representation as a string"""

        from io import StringIO

        s = StringIO()
        w = csv.writer(s)
        for row in self.rows:
            w.writerow(row)

        return s.getvalue()

    def as_lines(self):
        """Return a Lines representation as a string"""

        out_lines = []
        for t, v in self.lines:

            # Make the output prettier
            if t == 'Section':
                out_lines.append('')

            out_lines.append('{}: {}'.format(t, v if v is not None else ''))

        return '\n'.join(out_lines)

    def _write_path(self, path):

        if path:
            u = parse_app_url(str(path))
        else:
            u = self.ref

        if u.scheme != 'file':
            raise MetatabError("Can't write file to URL '{}'".format(str(path)))

        path = u.fspath

        if path is None:

            try:
                path = pathlib.Path(self.ref.fspath)
            except AttributeError:

                if isinstance(self.ref, str):
                    path = pathlib.Path(self.ref)
                else:
                    path = pathlib.Path(DEFAULT_METATAB_FILE)

            return path
        else:
            return pathlib.Path(str(path))

    def _write(self, content, path: pathlib.Path, ext=None):

        self.cleanse()

        debug_logger.debug("writing doc {}".format(str(path)))

        with path.open('wb') as f:
            f.write(content.encode('utf8'))

        return path

    def write_csv(self, path=None):

        path = self._write_path(path)

        if path.suffix != '.csv':
            raise MetatabError("Writing CSV file, but extension is wrong: {} ".format(str(path)))

        return self._write(self.as_csv(), path)

    def write_lines(self, path=None):

        path = self._write_path(path)

        if path.suffix != '.txt':
            raise MetatabError("Writing line (txt) file, but extension is wrong: {} ".format(str(path)))

        return self._write(self.as_lines(), path)

    def write(self, path=None):

        path = self._write_path(path)

        if path.suffix == '.txt':
            self.write_lines(path)
        elif path.suffix == '.csv':
            self.write_csv(path)
        else:
            raise FormatError("Can't write to filetype of {}".format(path.suffix))
