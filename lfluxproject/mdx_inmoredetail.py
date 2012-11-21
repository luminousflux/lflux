from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown import util

IMD_RE = r'<imd (.+)>'

class InmoredetailPattern(Pattern):
    def handleMatch(self, m):
        el = util.etree.Element("span")
        el.text = m.group(2)
        el.set('class', 'inmoredetail')

        return el

class InmoredetailExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.inlinePatterns.add('inmoredetail', InmoredetailPattern(IMD_RE), '_begin')

def makeExtension(configs=[]):
    return InmoredetailExtension(Extension)
