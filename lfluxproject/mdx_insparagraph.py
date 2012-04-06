import re
from markdown import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.preprocessors import Preprocessor
from markdown import etree_loader

__version__ = '0.1'


class InsParagraphProcessor(Treeprocessor):
    """ Process Paragraph blocks. """

    def run(self, root):
        for child in root:
            if (child.text or '').strip().startswith('.ins'):
                if root.tag == 'blockquote':  # nested pars. this might apply to more tags.
                    root.set('class','ins')
                else:
                    child.set('class', 'ins')
                child.text = child.text.strip()[5:]
            else:
                self.run(child)
        return root

class InsParagraphPreprocessor(Preprocessor):
    """ move .ins declaration inside block "tags" """
    def run(self, lines):
        BLOCKCHARS = ('=','>','*','+','-','#',)
        newlines = []
        for line in lines:
            if line.startswith('.ins ') and len(line)>6 and (line[4] in BLOCKCHARS or line[5] in BLOCKCHARS):
                idx = 5
                while len(line) > idx+1 and line[idx] in BLOCKCHARS:
                    idx+=1
                newline = line[5:idx] + ' .ins ' + line[idx:]
                newlines.append(newline)
            else:
                newlines.append(line)
        return newlines

        

class InsParagraphExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.treeprocessors['insparagraph'] = InsParagraphProcessor(md)
        md.preprocessors.insert(0,'insparagraph', InsParagraphPreprocessor(md))


def makeExtension(configs=[]):
    return InsParagraphExtension(configs=configs)
