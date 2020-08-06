import shutil

import nox


def docs_command(builder):
    return [
        "sphinx-build",
        "-b",
        builder,
        "docssrc/source",
        "docssrc/build/_build/{}".format(builder),
    ]


@nox.session
def docs(session):
    session.notify("docs_test")
    session.notify("docs_build")


DOC_REQUIRES = [
    "sphinx",
    "sphinx_rtd_theme",
    "sphinx-autodoc-typehints",
    "kecleon",
    "beautifulsoup4",
]


@nox.session(python="3.8")
def docs_test(session):
    session.install(*DOC_REQUIRES)
    shutil.rmtree("docssrc/build/", ignore_errors=True)
    session.run(*docs_command("doctest"))
    # session.run(*docs_command("linkcheck"))
    session.run(*docs_command("html"))
    shutil.rmtree("docssrc/build/", ignore_errors=True)


@nox.session(python="3.8")
def docs_build(session):
    session.install(*DOC_REQUIRES)
    shutil.rmtree("docs/", ignore_errors=True)
    session.run("sphinx-build", "-b", "html", "docssrc/source", "docs", "-a")
