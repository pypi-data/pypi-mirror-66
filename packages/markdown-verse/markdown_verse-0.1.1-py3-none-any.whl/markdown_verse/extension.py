import re
import xml.etree.ElementTree as etree

from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor


TAG = 'div'
CLASS = 'verse'


class VerseExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'tag': [TAG,
                'The tag name used to wrap the verse block'],
            'tag_class': [CLASS,
                'The CSS class used on that tag'],
        }
        super(VerseExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, what):
        md.parser.blockprocessors.register(
            VerseProcessor(
                self.getConfig('tag'),
                self.getConfig('tag_class'),
                md.parser),
            'verse', 175)


class VerseProcessor(BlockProcessor):

    VERSE_RE = re.compile(r'''^(?P<quotes>'{3})\n(?P<body>.*?)\n(?P=quotes)$''',
                          re.DOTALL | re.MULTILINE)
    def __init__(self, tag, tag_class, *args, **kwargs):
        self.tag = tag
        self.tag_class = tag_class
        super().__init__(*args, **kwargs)

    def test(self, parent, block):
        return self.VERSE_RE.search(block)

    def run(self, parent, blocks):
        sibling = self.lastChild(parent)
        block = blocks.pop(0)
        m = self.VERSE_RE.search(block)
        if m:
            block = m.group('body')
            el = etree.SubElement(parent, self.tag)
            el.text = block
            if self.tag_class:
                el.set('class', self.tag_class)
        else:
            el = sibling

def makeExtension(**kwargs):
    return VerseExtension(**kwargs)
