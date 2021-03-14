import enum
import string
import textwrap
import dataclasses

import yaml

from docutils import nodes

from .file_cache import get_post_license, get_post_title, get_user_name, get_question_id, get_author_id


class LinkTypes(enum.Enum):
    NAMED = ""
    QUESTION = "Question "
    ANSWER = "Answer to "


LICENSE_TABLE = str.maketrans(
    string.ascii_lowercase,
    string.ascii_uppercase,
    " -.",
)

LINK_PREFIX = {
    LinkTypes.NAMED: "",
    LinkTypes.QUESTION: "Question ",
    LinkTypes.ANSWER: "Answer to ",
}


class ReferencesBuilder:
    def load(self, path):
        with open(path) as f:
            references = []
            for reference in yaml.safe_load(f):
                _reference = {}
                self._set_page(reference, _reference)
                self._set_link(reference, _reference)
                self._set_user(reference, _reference)
                self._set_license(reference, _reference)
                self._set_section(reference, _reference)
                self._set_quote(reference, _reference)
                references.append(_reference)
            return references

    def _get_question_id(self, answer):
        return get_question_id(answer)

    def _get_question_name(self, question):
        return get_post_title(question)

    def _get_question_link(self, question):
        return f"https://codereview.meta.stackexchange.com/q/{question}/42401"

    def _get_answer_link(self, answer):
        return f"https://codereview.meta.stackexchange.com/a/{answer}/42401"

    def _get_user_name(self, user):
        return get_user_name(user)

    def _get_user_link(self, user):
        return f"https://codereview.meta.stackexchange.com/users/{user}"

    def _get_user_id(self, question_id, post_id):
        return get_author_id(question_id, post_id)

    def _get_post_license(self, q_id, id):
        return get_post_license(q_id, id)

    def _get_license(self, license):
        license = license.translate(LICENSE_TABLE)
        return {
            "CCBYSA2": ("CC BY-SA 2.5", "https://creativecommons.org/licenses/by-sa/2.5/"),
            "CCBYSA25": ("CC BY-SA 2.5", "https://creativecommons.org/licenses/by-sa/2.5/"),
            "CCBYSA3": ("CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0/"),
            "CCBYSA30": ("CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0/"),
            "CCBYSA4": ("CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0/"),
            "CCBYSA40": ("CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0/"),
        }[license]

    def _set_page(self, src, dest):
        dest["page"] = src["page"]
        dest["item"] = src["item"]

    def _set_link(self, src, dest):
        name = src.get("name")
        link = src.get("link")
        question = src.get("question")
        answer = src.get("answer")
        if ((
                None is name
                or None is link
            )
            and None is question
            and None is not answer
        ):
            src["question"] = question = self._get_question_id(answer)
        type = LinkTypes.NAMED
        if None is name:
            type = (
                LinkTypes.ANSWER
                if "answer" in src else
                LinkTypes.QUESTION
            )
            if None is not question:
                name = self._get_question_name(question)
        if None is link:
            if None is not answer:
                link = self._get_answer_link(answer)
            elif None is not question:
                link = self._get_question_link(question)
        if (None is name
            or None is link
        ):
            dest["link"] = Null()
        else:
            dest["link"] = Link(
                name,
                link,
                name_prefix=LINK_PREFIX[type]
            )

    def _set_user(self, src, dest):
        user = src.get("user")
        question = src.get("question")
        answer = src.get("answer")
        if (None is user
            and (
                None is not question
                or None is not answer
            )
        ):
            user = self._get_user_id(question, answer or question)
        if None is user:
            dest["user"] = Null()
        else:
            dest["user"] = Link(
                self._get_user_name(user),
                self._get_user_link(user),
                prefix=" by ",
            )

    def _set_license(self, src, dest):
        license = src.get("license")
        question = src.get("question")
        post = src.get("answer") or question
        if (None is license
            and None is not post
        ):
            license = self._get_post_license(question, post)
        if None is license:
            dest["license"] = Null()
        else:
            name, link = self._get_license(license)
            dest["license"] = Link(
                name,
                link,
                prefix=" © ",
            )

    def _set_section(self, src, dest):
        if None is (section := src.get("section")):
            dest["section"] = Null()
        else:
            dest["section"] = Text(section, ' under "{}"')

    def _set_quote(self, src, dest):
        if None is (quote := src.get("quote")):
            dest["quote"] = Null()
        else:
            dest["quote"] = Quote(quote)

    def format_reference(self, reference):
        return "".join([
            reference.get("link", Null()).as_string(),
            reference.get("section", Null()).as_string(),
            reference.get("user", Null()).as_string(),
            reference.get("license", Null()).as_string(),
            reference.get("quote", Null()).as_string(),
        ])

    def messages(self, references):
        for reference in references:
            yield {
                "page": reference["page"],
                "item": reference["item"],
                "message": self.format_reference(reference),
            }


@dataclasses.dataclass
class Link:
    name: str
    link: str
    prefix: str = ""
    suffix: str = ""
    name_prefix: str = ""
    name_suffix: str = ""

    def as_string(self):
        return "{}`{}{}{} <{}>_`{}".format(
            self.prefix,
            self.name_prefix,
            self.name,
            self.name_suffix,
            self.link,
            self.suffix,
        )

    def as_nodes(self):
        if prefix := self.prefix:
            yield nodes.Text(prefix)
        name = self.name_prefix + self.name + self.name_suffix
        link = self.link
        yield nodes.reference('', name, internal=False, refuri=link, reftitle=self.name)
        if suffix := self.suffix:
            yield nodes.Text(suffix)


@dataclasses.dataclass
class Text:
    text: str
    format: str = "{}"

    def as_string(self):
        return self.format.format(self.text)

    def as_nodes(self):
        yield nodes.Text(self.format.format(self.text))


@dataclasses.dataclass
class Null:
    def as_string(self):
        return ""

    def as_nodes(self):
        return []


@dataclasses.dataclass
class Quote:
    quote: str

    def as_string(self):
        return "\n\n" + textwrap.indent(self.quote, "    ")

    def as_nodes(self):
        yield nodes.block_quote("", nodes.Text(self.quote))


class References:
    BUILDER = ReferencesBuilder()

    def __init__(self, references, *, builder=None):
        self._references = references
        if None is not builder:
            self.BUILDER = builder

    def __iter__(self):
        return iter(self._references)

    @classmethod
    def load(cls, path, *, builder=None):
        if None is builder:
            builder = cls.BUILDER
        return cls(builder.load(path), builder=builder)

    def messages(self):
        return type(self)(
            self.BUILDER.messages(self._references),
            builder=self.BUILDER
        )

    def group(self):
        groups = {}
        for reference in self._references:
            page = reference.pop("page")
            item = reference.pop("item")
            (
                groups
                    .setdefault(page, {})
                    .setdefault(item, [])
                    .append(reference)
            )
        return {
            key: {
                str(item): group[item]
                for item in sorted(group)
            }
            for key, group in groups.items()
        }
