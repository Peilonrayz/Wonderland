import shutil

import nox

DOC_REQUIRES = [
    "sphinx==3.1.2",
    "sphinx_rtd_theme",
    "sphinx-autodoc-typehints",
]


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
    session.notify("docs_clean_build")


@nox.session(python="3.9")
def docs_test(session):
    session.install(*DOC_REQUIRES)
    session.install("-e", ".")
    shutil.rmtree("docssrc/build/", ignore_errors=True)
    session.run(*docs_command("doctest"))
    # session.run(*docs_command("linkcheck"))
    session.run(*docs_command("html"))
    shutil.rmtree("docssrc/build/", ignore_errors=True)


@nox.session
def docs_clean_build(session):
    shutil.rmtree("docs/", ignore_errors=True)
    session.notify("docs_build")


@nox.session(python="3.9")
def docs_build(session):
    session.install(*DOC_REQUIRES)
    session.install("-e", ".")
    session.run("sphinx-build", "-b", "html", "docssrc/source", "docs", "-a")
