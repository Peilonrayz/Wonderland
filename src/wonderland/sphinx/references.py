import pathlib

from docutils import nodes

from ..extracters import References, Null

CWD = pathlib.Path.cwd()
DOCS_SRC = CWD / "docssrc" / "source"

REFERENCES = References.load("references.yaml").group()


def reference_group(name, rawtext, text, lineno, inliner, options={}, content=[]):
    path = inliner.document.current_source
    path = str(pathlib.Path(path).relative_to(DOCS_SRC))
    _refs = REFERENCES.get(path, {}).get(text, [])
    if not _refs:
        return ([], [])
    container = nodes.enumerated_list()
    for ref in _refs:
        output = [
            *ref.get("link", Null()).as_nodes(),
            *ref.get("section", Null()).as_nodes(),
            *ref.get("user", Null()).as_nodes(),
            *ref.get("license", Null()).as_nodes(),
        ]
        if Null() == (quote := ref.get("quote", Null())):
            message = nodes.paragraph()
            for node in output:
                message.append(node)
        else:
            message = nodes.line_block(
                "",
                nodes.line("", "", *output),
                nodes.line(
                    "",
                    "",
                    *quote.as_nodes(),
                )
            )
        container.append(nodes.list_item('', message))
    return ([container], [])
