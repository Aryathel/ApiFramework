# Credit to sphinx.ext.extlinks for being a good starter
# Copyright 2007-2020 by the Sphinx team
# Licensed under BSD.

from typing import Any, Dict, List, Tuple
import re
import importlib
import inspect
from collections import OrderedDict

from docutils import nodes, utils
from docutils.nodes import Node, system_message
from docutils.parsers.rst.states import Inliner

import sphinx
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.util.nodes import split_explicit_title
from sphinx.util.typing import RoleFunction
from sphinx.util.docutils import SphinxDirective
from sphinx.ext import extlinks


_name_parser_regex = re.compile(r'(?P<module>[\w.]+\.)?(?P<name>\w+)')


def make_link_role(resource_links: Dict[str, str]) -> RoleFunction:
    def role(
        typ: str,
        rawtext: str,
        text: str,
        lineno: int,
        inliner: Inliner,
        options: Dict = {},
        content: List[str] = []
    ) -> Tuple[List[Node], List[system_message]]:

        text = utils.unescape(text)
        has_explicit_title, title, key = split_explicit_title(text)
        full_url = resource_links[key]
        if not has_explicit_title:
            title = full_url
        pnode = nodes.reference(title, title, internal=False, refuri=full_url)
        return [pnode], []
    return role


def add_link_role(app: Sphinx) -> None:
    app.add_role('resource', make_link_role(app.config.resource_links))


class inheritedlinkplaceholder(nodes.General, nodes.Element):
    pass


class InheritedClass(SphinxDirective):
    has_content = False
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {}

    def parse_name(self, content):
        path, name = _name_parser_regex.match(content).groups()
        if path:
            modulename = path.rstrip('.')
        else:
            modulename = self.env.temp_data.get('autodoc:module')
            if not modulename:
                modulename = self.env.ref_context.get('py:module')
        if modulename is None:
            raise RuntimeError('modulename somehow None for %s in %s.' % (content, self.env.docname))

        return modulename, name

    def run(self):
        args = [arg.strip().rstrip(',') for arg in self.arguments]
        node_list = []

        if len(args) == 1:
            content = args[0].strip()
            modulename, name = self.parse_name(content)
            node = inheritedlinkplaceholder('')
            node['text'] = name
            node['ref'] = f"{modulename}.{name}"

            node_list.append(node)
        elif len(args) == 2:
            text = args[1].strip()
            content = args[0].strip()
            modulename, name = self.parse_name(content)

            node = inheritedlinkplaceholder('')
            node['text'] = text
            node['ref'] = f"{modulename}.{name}"

            node_list.append(node)

        return node_list


class StaticExternalInheritedClass(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        'objtype': str,
        'link': str
    }

    def run(self):
        try:
            objtype = self.options['objtype'].strip()
            link = self.options['link'].strip()
            text = '\n'.join(self.content) if self.content else link

        except KeyError as e:
            raise KeyError(f"{self.env.temp_data['docname']} {self.env.temp_data['object']}: {e.args[0]}")

        return [results_to_node(text, obj_type=objtype, uri=link, internal=False)]


class ExternalInheritedClass(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        'objtype': str,
        'extlink-root': str,
        'extlink-path': str
    }

    def run(self):
        try:
            objtype = self.options['objtype'].strip()
            form = self.options['extlink-root'].strip()
            form = self.config.extlinks[form]
            link = form[0] % self.options['extlink-path'].strip()
            text = '\n'.join(self.content) if self.content else link

        except KeyError as e:
            raise KeyError(f"{self.env.temp_data['docname']} {self.env.temp_data['object']}: {e.args[0]}")

        return [results_to_node(text, obj_type=objtype, uri=link, internal=False)]


def results_to_node(text, obj_type="", docname=None, fullname=None, uri=None, internal=True):
    label = nodes.Text(f'This{" " + obj_type if not obj_type == "" else ""} inherits from ')
    ref = nodes.reference(
        text,
        '',
        internal=internal,
        refuri=f'{docname}.html#{fullname}' if not uri else uri,
        anchorname='',
        *[nodes.Text(text)]
    )
    period = nodes.Text('.')

    node = nodes.line_block('')
    node.append(nodes.emphasis('', *[label, ref, period]))
    return node


def build_lookup_table(env):
    # Given an environment, load up a lookup table of
    # full-class-name: objects
    results = {}
    parameters = {}
    domain = env.domains['py']

    for (fullname, _, objtype, docname, _, _) in domain.get_objects():
        if not objtype == 'parameter':
            results[fullname] = {
                "type": objtype,
                "docname": f'{docname}',
                "ref": fullname
            }
        else:
            parameters[fullname.replace('.params', '')] = {
                "type": objtype,
                "docname": f'{docname}',
                "ref": fullname
            }

    return results, parameters


def process_inherited_classes(app, doctree, fromdocname):
    env = app.builder.env

    lookup, params = build_lookup_table(env)

    node_list = doctree.traverse(inheritedlinkplaceholder)
    for node in node_list:
        ref = node['ref']
        attr = lookup.get(ref, params.get(ref))
        if not attr:
            raise IndexError(f'Object {ref} could not be found.')
        objtype = attr['type']
        docname = attr['docname']

        new_node = results_to_node(
            node['text'],
            obj_type=objtype,
            docname=docname,
            fullname=attr['ref']
        )

        node.replace_self([new_node])


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_config_value('resource_links', {}, 'env')
    app.connect('builder-inited', add_link_role)

    app.add_directive('inherits_from', InheritedClass)
    app.add_directive('external_inherits_from', ExternalInheritedClass)
    app.add_directive('static_inherits_from', StaticExternalInheritedClass)

    app.add_node(inheritedlinkplaceholder)

    app.connect('doctree-resolved', process_inherited_classes)

    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
