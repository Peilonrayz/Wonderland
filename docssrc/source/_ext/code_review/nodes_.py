from docutils import nodes


class Post(nodes.TextElement):
    def __init__(self, uri, text='', title=''):
        super().__init__()
        self._ref = nodes.reference('', text, internal=False, refuri=uri, reftitle=title)
        super().append(self._ref)

    def append(self, value):
        self._ref.append(value)


# https://codereview.meta.stackexchange.com/questions/tagged/{}
class Tag(nodes.Element):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag


class MTag(nodes.Element):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag
