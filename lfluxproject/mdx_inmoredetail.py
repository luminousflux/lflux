from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown.treeprocessors import Treeprocessor
from markdown import util

IMD_RE = r'<imd (.+)>'

class InmoredetailPattern(Pattern):
    """ deprecated <imd ....> syntax """
    def handleMatch(self, m):
        el = util.etree.Element("span")
        el.text = m.group(2)
        el.set('class', el.get('class', '') + ' inmoredetail')

        return el

class InmoredetailTreeProcessor(Treeprocessor):
    def _find_elem(self, tree, text):
        tree.text = tree.text or ''
        if text in tree.text:
            return [tree]
        if text in (tree.tail or ''):
            return [tree]
        for child in tree.getchildren():
            x = self._find_elem(child, text)
            if x:
                return [tree] + x
        return None

    def _find_start(self, tree):
        return self._find_elem(tree, '[imd]')
    def _find_end(self, tree):
        return self._find_elem(tree, '[/imd]')

    def _wrap_in_span(self, text, imdcount):
        newelem = util.etree.Element('span')
        newelem.text = text
        newelem.set('class', 'inmoredetail imd-%s' % imdcount)
        return newelem


    def _walk(self, start_tree, end_tree, imdcount):
        depth = 0
        for i in range(len(start_tree)):
            if start_tree[:i] == end_tree[:i]:
                depth = i

        current = start_tree
        i = len(current)
        """ going left, to the depth where we can traverse to end_tree """
        while i > depth+1:
            x = current.pop()
            if x.tail and x.tail.strip():
                newelem = self._wrap_in_span(x.tail, imdcount)
                x.tail = None
                x.append(newelem)
            i = len(current)
            parent = current[-1]
            children = parent.getchildren()
            ind = children.index(x)
            restchildren = children[ind+1:]

            for child in restchildren:
                child.set('class', child.get('class', '') + ' inmoredetail imd-%s' % imdcount)
                if child.tail and child.tail.strip():
                    newelem = self._wrap_in_span(child.tail, imdcount)
                    child.tail = None
                    child.append(newelem)
        """ traversing the siblings """
        x = current.pop()
        children = current[-1].getchildren()
        while True and len(children)>children.index(x)+1:
            x = children[children.index(x)+1]
            if x==end_tree[len(current)]:
                break
            x.set('class', x.get('class', '') + ' inmoredetail imd-%s' % imdcount)

        """ going down to the end point """
        for i in range(depth+1, len(end_tree)):
            parent = end_tree[i-1]
            children = parent.getchildren()
            x = end_tree[i]
            index = children.index(x)
            for j in range(index-1):
                x = children[j]
                x.set('class', x.get('class','') + ' inmoredetail imd-%s' % imdcount)
                if x.tail and x.tail.strip():
                    newelem = self._wrap_in_span(x.tail, imdcount)
                    x.tail = None
                    x.append(newelem)
            if parent.text and parent.text.strip():
                newelem = self._wrap_in_span(parent.text, imdcount)
                parent.text = ''
                parent.insert(0, newelem)
        parent = end_tree[-1]
        is_tail = not('[/imd]' in parent.text)
        if is_tail:
            before, after = parent.tail.split('[/imd]',1)
            parent.tail = ''
            parent.set('class', parent.get('class','') + 'inmoredetail imd-%s' % imdcount)
            newelem = self._wrap_in_span(before, imdcount)
            newelem.tail = after
            end_tree[-2].insert(end_tree[-2].getchildren().index(parent)+1, newelem)
        else:
            before, after = parent.text.split('[/imd]',1)
            parent.text = after
            newelem = self._wrap_in_span(before, imdcount)
            parent.insert(0, newelem)


    def run(self, root):
        x = True
        imdcount = 0
        while x:
            x = self._find_start(root)
            if x:
                parent,elem = x[-2:]
                is_tail = not ('[imd]' in elem.text)
                if not is_tail:
                    before, after = elem.text.split('[imd]',1)
                    elem.text = before
                    newelem = self._wrap_in_span(after, imdcount)
                    elem.append(newelem)
                else:
                    before, after = elem.tail.split('[imd]',1)
                    elem.tail = before
                    elemindex = parent.getchildren().index(elem)
                    newelem = self._wrap_in_span(after, imdcount)
                    parent.insert(elemindex+1, newelem)
                if is_tail:
                    x.pop()
                if '[/imd]' in newelem.text:
                    index = newelem.text.index('[/imd]')
                    newelem.text,newelem.tail = newelem.text[0:index],newelem.text[index+6:]
                else:
                    for i in range(len(x)):
                        y = self._find_end(x[-i])
                        if y:
                            self._walk(x+[newelem],y, imdcount)
                            break
            imdcount += 1

        return root

class InmoredetailExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.inlinePatterns.add('inmoredetail', InmoredetailPattern(IMD_RE), '_begin')
        md.treeprocessors.add('inmoredetial', InmoredetailTreeProcessor(), '_end')

def makeExtension(configs=[]):
    return InmoredetailExtension(Extension)
