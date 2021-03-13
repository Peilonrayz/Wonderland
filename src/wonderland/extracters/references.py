import enum
import string
import textwrap

import yaml


class Link(enum.Enum):
    NAMED = 0
    QUESTION = 1
    ANSWER = 2


LICENSE_TABLE = str.maketrans(
    string.ascii_lowercase,
    string.ascii_uppercase,
    " -.",
)

LINK_PREFIX = {
    Link.NAMED: "",
    Link.QUESTION: "Question ",
    Link.ANSWER: "Answer to ",
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
        return answer  # TODO: properly implement

    def _get_question_name(self, question):
        return question  # TODO: properly implement

    def _get_question_link(self, question):
        return f"https://codereview.meta.stackexchange.com/q/{question}/42401"

    def _get_answer_link(self, answer):
        return f"https://codereview.meta.stackexchange.com/a/{answer}/42401"

    def _get_user_name(self, user):
        return user  # TODO: properly implement

    def _get_user_link(self, user):
        return f"https://codereview.meta.stackexchange.com/users/{user}"

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
            question = self._get_question_id(answer)
        type = Link.NAMED
        if None is name:
            type = (
                Link.ANSWER
                if "answer" in src else
                Link.QUESTION
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
            dest["link"] = None
        else:
            dest["link"] = {
                "name": name,
                "link": link,
                "type": type,
            }

    def _set_user(self, src, dest):
        if None is (user := src.get("user")):
            dest["user"] = None
        else:
            dest["user"] = {
                "name": self._get_user_name(user),
                "link": self._get_user_link(user),
            }

    def _set_license(self, src, dest):
        if None is (license := src.get("license")):
            dest["license"] = None
        else:
            name, link = self._get_license(license)
            dest["license"] = {
                "name": name,
                "link": link,
            }

    def _set_section(self, src, dest):
        dest["section"] = src.get("section")

    def _set_quote(self, src, dest):
        dest["quote"] = src.get("quote")

    def _format_link(self, link, fmt="`{name} <{link}>`_", /, **kwargs):
        if None is link:
            return []
        return [
            fmt.format(
                name=link["name"],
                link=link["link"],
                **{
                    name: fn(link.get(name))
                    for name, fn in kwargs.items()
                },
            ),
        ]

    def _normalize_quote(self, quote):
        return textwrap.indent(quote, "    ")

    def format_reference(self, reference):
        output = []
        output.extend(self._format_link(
            reference.get("link"),
            "`{type}{name} <{link}>`_",
            type=lambda t: LINK_PREFIX[t],
        ))
        if None is not (section := reference.get("section")):
            output.append(f' under "{section}"')
        output.extend(self._format_link(
            reference.get("user"),
            " by `{name} <{link}>`_",
        ))
        output.extend(self._format_link(
            reference.get("license"),
            " © `{name} <{link}>`_",
        ))
        if None is not (quote := reference.get("quote")):
            output.append(f"\n\n{self._normalize_quote(quote)}")
        return "".join(output)

    def messages(self, references):
        for reference in references:
            yield {
                "page": reference["page"],
                "item": reference["item"],
                "message": self.format_reference(reference),
            }


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
                item: group[item]
                for item in sorted(group)
            }
            for key, group in groups.items()
        }


def load(path, *, builder=None):
    return References.load(path, builder=builder)
