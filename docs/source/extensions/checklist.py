from docutils import nodes
import re
from sphinx.util.docutils import SphinxDirective

class checklist(nodes.General, nodes.Element):
    pass

class checklist_item(nodes.Part, nodes.Element):
    pass

def visit_checklist_node(self, node):
    self.body.append(self.starttag(node, 'ul', CLASS='checklist'))

def visit_checklist_item(self, node):
    checked = "checked" if node['check_line_type'] == 'check' else "unchecked"

    self.body.append(self.starttag(node, 'li'))

    self.body.append(
        f'<span class="checklist-item {checked}">\n'
        f'  {node["check_label"]}\n'
        f'</span>\n'
    )

def depart_checklist_item(self, node):
    self.body.append('</li>\n')

def depart_checklist_node(self, node):
    self.body.append('</ul>\n')


_checkbox_pattern = re.compile(r'((?P<check>:check:)|(?P<uncheck>:uncheck:))?(`(?P<label>.*)`)')


class Checklist(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    indentation: int = None

    def parse_indentation(self, line):
        stripped = line.lstrip(' ')
        indent = len(line) - len(stripped)
        if indent > 0:
            if not self.indentation:
                self.indentation = indent
                indent = 1
            else:
                indent //= self.indentation

        return indent, line.strip()

    def parse_line(self, line):
        groups = _checkbox_pattern.match(line).groupdict()
        line_type = None
        if groups.get('check'):
            line_type = 'check'
        elif groups.get('uncheck'):
            line_type = 'uncheck'
        label = groups.get('label')
        return line_type, label

    def get_children(self, root, node_list):
        node_items = []
        while len(node_list) > 0:
            if node_list[0]['check_indent'] <= root['check_indent']:
                break

            parent = node_list.pop(0)

            child = self.get_children(parent, node_list)
            if child:
                parent.append(child)

            node_items.append(parent)

        node = None
        if node_items:
            node = checklist('')
            for item in node_items:
                node.append(item)

        return node

    def organize_nodes(self, node_list):
        node_items = checklist('')

        while len(node_list) > 0:
            parent = node_list.pop(0)

            child = self.get_children(parent, node_list)
            if child:
                parent.append(child)

            node_items.append(parent)

        return node_items

    def run(self):
        self.assert_has_content()

        items = [self.parse_indentation(l) for l in self.content]
        node_list = []
        for indent, line in items:
            line_type, label = self.parse_line(line)

            node = checklist_item('')
            node['check_line_type'] = line_type
            node['check_indent'] = indent
            node['check_label'] = label
            node_list.append(node)

        node_list = self.organize_nodes(node_list)

        return [node_list]


def setup(app):
    app.add_node(checklist, html=(visit_checklist_node, depart_checklist_node))
    app.add_node(checklist_item, html=(visit_checklist_item, depart_checklist_item))
    app.add_directive('checklist', Checklist)
