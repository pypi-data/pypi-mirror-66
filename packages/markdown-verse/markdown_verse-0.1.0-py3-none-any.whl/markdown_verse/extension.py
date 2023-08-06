import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor


TAG_TUPLE = ('<div class="verse">', '</div>')


class VerseExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'tag_tuple': [TAG_TUPLE,
                'The start- and end-tags used to wrap the verse block'],
        }
        super(VerseExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.preprocessors.register(VersePreprocessor(self.getConfig('tag_tuple')), 'verse', 20)


class VersePreprocessor(Preprocessor):

    VERSE_RE = re.compile(r'''(?P<quotes>'{3})\n(?P<body>.*?)\n(?P=quotes)''', re.DOTALL)

    def __init__(self, tag_tuple, *args, **kwargs):
        self.tag_tuple = tag_tuple
        super(VersePreprocessor, self).__init__(*args, **kwargs)
    
    def repl(self, match_groups):
        return '{}{}{}'.format(
            self.tag_tuple[0],
            match_groups.group('body'),
            self.tag_tuple[1])

    def run(self, lines):
        text = '\n'.join(lines)
        text = re.sub(self.VERSE_RE, self.repl, text)
        return text.split('\n')


def makeExtension(**kwargs):
    return VerseExtension(**kwargs)
