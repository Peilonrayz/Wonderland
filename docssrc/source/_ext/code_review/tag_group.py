import csv
import pathlib

from docutils import nodes

from . import cache
from .nodes_ import Post, MTag


def make_item(id, tags):
    name = cache.get(str(id), cache.title)
    link = f'https://codereview.meta.stackexchange.com/q/{id}/42401'
    post = Post(link, name, name)
    if not tags:
        inner = nodes.paragraph()
        inner.append(post)
    else:
        inner = nodes.line_block(
            '',
            nodes.line('', '', post),
            nodes.line(
                '',
                '', 
                *(MTag(t) for t in tags),
            )
        )
    return nodes.list_item('', inner)


def make_items(items):
    ret = nodes.bullet_list()
    for id, tags in items:
        ret.append(make_item(id, tags))
    return ret


def read_csv():
    with (pathlib.Path.cwd() / 'tags.csv').open(newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for id, *tags in reader:
            yield int(id), [t for t in tags if t]


def build_tags(search):
    tags = [set(), set()]
    for t in search.split(','):
        if t.startswith('!'):
            tags[1].add(t[1:])
        else:
            tags[0].add(t)
    return tags


def filter_tags(wanted, not_wanted, rows):
    for id, tags in rows:
        t = set(tags)
        if wanted <= t and not t & not_wanted:
            yield id, tags


def tag_group(name, rawtext, text, lineno, inliner, options={}, content=[]):
    wanted, not_wanted = build_tags(text)
    items = filter_tags(wanted, not_wanted, read_csv())
    return (
        [make_items(sorted(items))],
        [],
    )
