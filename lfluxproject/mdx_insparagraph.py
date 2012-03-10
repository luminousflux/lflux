import re
from markdown import Extension
from markdown.treeprocessors import Treeprocessor
from markdown import etree_loader

__version__ = '0.1'


class InsParagraphProcessor(Treeprocessor):
    """ Process Paragraph blocks. """

    def run(self, root):
        for child in root:
            if (child.text or '').strip().startswith('.ins'):
                child.set('class', 'ins')
                child.text.replace('.ins','')
            else:
                self.run(child)
        return root

class InsParagraphExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.treeprocessors['insparagraph'] = InsParagraphProcessor(md)


def makeExtension(configs=[]):
    return InsParagraphExtension(configs=configs)
