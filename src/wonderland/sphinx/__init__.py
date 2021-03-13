import pathlib

from docutils import nodes

from sphinx.application import Sphinx

from .. import extracters
from .nodes_ import Post, Tag, MTag
from .tag_group import tag_group


def visit_post_html(self, node):
    pass
def depart_post_html(self, node):
    pass


def visit_tag_html(self, node):
    self.body.append(f'[{node.tag}]')
    raise nodes.SkipNode


def visit_mtag_html(self, node):
    self.body.append(self.starttag(node, 'span', **{'class': 'tag'}))
    self.body.append(node.tag)
    self.body.append('</span>')
    raise nodes.SkipNode


def post(name, rawtext, text, lineno, inliner, options={}, content=[]):
    name = extracters.get_post_title(text)
    link = f'https://codereview.meta.stackexchange.com/q/{text}/42401'
    return (
        [Post(link, name, name)],
        [],
    )


def tag(name, rawtext, text, lineno, inliner, options={}, content=[]):
    return (
        [Tag(text)],
        [],
    )


def mtag(name, rawtext, text, lineno, inliner, options={}, content=[]):
    return (
        [MTag(text)],
        [],
    )


def setup(app: Sphinx):
    app.config._raw_config.setdefault('html_static_path', []).insert(
        0,
        str(pathlib.Path(__file__).parent / '_static'),
    )
    app.add_css_file('code_review.css')

    app.add_node(Post, html=(visit_post_html, depart_post_html))
    app.add_node(Tag, html=(visit_tag_html, None))
    app.add_node(MTag, html=(visit_mtag_html, None))

    app.add_role('post', post)
    app.add_role('tag', tag)
    app.add_role('mtag', mtag)
    app.add_role('tag_group', tag_group)
