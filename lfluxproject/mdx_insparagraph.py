import re
import markdown
from markdown import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.preprocessors import Preprocessor
from markdown.inlinepatterns import SimpleTagPattern
from markdown import etree_loader

__version__ = '0.1'


class InsParagraphProcessor(Treeprocessor):
    """ Process Paragraph blocks. """

    def run(self, root):
        for child in root:
            if (child.text or '').lstrip().startswith('.ins'):
                if root.tag == 'blockquote':
                    # nested pars. this might apply to more tags.
                    root.set('class', root.get('class','') + ' ins')
                else:
                    child.set('class', child.get('class', '') + ' ins')
                child.text = child.text.lstrip()[5:]
            elif child.tag == 'ins' and len(root.getchildren())==1 and (not child.tail or not child.tail.strip()):
                root.set('class', root.get('class','') + ' ins')
                child.tag = 'span'
            else:
                self.run(child)
        return root


class InsParagraphPreprocessor(Preprocessor):
    RE = re.compile(r'^\.ins\s*([ ]{0,3}\[([^\]]*)\]:\s*([^ ]*)[ ]*(%s)?)$' % markdown.preprocessors.ReferencePreprocessor.TITLE, re.DOTALL)
    """ move .ins declaration inside block "tags" """
    def run(self, lines):
        BLOCKCHARS = ('=', '>', '*', '+', '-', '#', )
        newlines = []
        for line in lines:
            if self.RE.match(line):
                newlines.append(self.RE.match(line).groups()[0])
                continue
            if line.startswith('.ins ') and len(line) > 6 and (
                    line[4] in BLOCKCHARS or line[5] in BLOCKCHARS):
                idx = 5
                while len(line) > idx + 1 and line[idx] in BLOCKCHARS:
                    idx += 1
                newline = line[5:idx] + ' .ins ' + line[idx:]
                newlines.append(newline)
            else:
                newlines.append(line)
        return newlines

class IMDPattern(SimpleTagPattern, object):
    def handleMatch(self, m):
        print 'match!', m.groups()
        return super(IMDPattern, self).handleMatch(m)

class InsParagraphExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.treeprocessors['insparagraph'] = InsParagraphProcessor(md)
        md.preprocessors.insert(0, 'insparagraph',
                                InsParagraphPreprocessor(md))



def makeExtension(configs=[]):
    return InsParagraphExtension(configs=configs)
