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
        x = self._has_tag(tree)
        if x is not None:
            return x
        for elem in tree.getchildren():
            return self._find_elem(elem, text)

        

    def _has_tag(self, elem, text):
        elem.text = elem.text or ''
        if text in elem.text:
            return elem, 'text'
        if text in (elem.tail or ''):
            return elem, 'tail'
        return None,None

    def _find_start(self, tree):
        return self._find_elem(tree, '[imd]')
    def _find_end(self, tree):
        return self._find_elem(tree, '[/imd]')

    def _is_start(self, elem):
        x,y = self._has_tag(elem, '[imd]')

        return x,y
    def _is_end(self, elem):
        return self._has_tag(elem, '[/imd]')

    def _set_class(self, elem, cls=None):
        elem.set('class', elem.get('class','') + (cls if cls is not None else ' inmoredetail imd-%s' % self.imdcount))

    def _wrap_in_span(self, text, cls=None):
        newelem = util.etree.Element('span')
        newelem.text = text
        self._set_class(newelem, cls)
        return newelem

    def _mark(self, parent, elem, mark_self, mark_tail):
        return mark_self+[elem], mark_tail+[(elem,parent,)]


    def _walk(self, parent, root, start, end, mark_self, mark_tail):
        """
            
            a
                b
                    c
                        d
                        d.tail
                    c.tail
                    e - START       - not start_set, not end_set, start, not end
                        f           - start_set, not end_set, start, not end
                        f.tail
                    e.tail
                    g
                    g.tail
                b.tail
                h
                h.tail
                j
                j.tail
                k
                    l
                        m
                        m.tail
                    l.tail
                    n
                    n.tail
                k.tail
                o
                o.tail
                p
                    q
                        r
                        r.tail
                    q.tail
                    s - END
                    s.tail
                    t
                    t.tail
                p.tail
                u
                u.tail

        """
        start_set = bool(start)
        end_set = bool(end)

        if start_set and end_set:
            return start, end, mark_self, mark_tail
        if not start_set and end_set:
            return start, end, mark_self, mark_tail


        if start_set:
            e,ewhere = self._is_end(root)
            if ewhere:
                end.append((e, parent,))
                mark_self = mark_self + [root]
                if ewhere=='tail':
                    mark_tail = mark_tail + [(root, parent,)]
                    for child in root.getchildren():
                        mark_self, mark_tail = self._mark(root, child, mark_self, mark_tail)
                return start, end, mark_self, mark_tail
        else:
            s,swhere = self._is_start(root)
            if swhere:
                start.append((s,parent,))
                
                e,ewhere = self._is_end(root)
                if ewhere:
                    end.append((e,parent,))

                if swhere=='text':
                    mark_self = mark_self + [root]
                if swhere=='tail' or ewhere=='tail':
                    mark_tail = mark_tail + [(root, parent,)]

                if ewhere and swhere!=ewhere:
                    for child in root.getchildren():
                        mark_self, mark_tail = self._mark(root, child, mark_self, mark_tail)

                if swhere=='tail' or ewhere:
                    return start, end, mark_self, mark_tail

        for child in root.getchildren():
            start, end, mark_self, mark_tail = self._walk(root, child, start, end, mark_self, mark_tail)
            if start and end:
                break
        if start and not end:
            if start_set:
                mark_self = list(set(mark_self + [root]))
            mark_tail = list(set(mark_tail + [(root,parent,)]))
        return start, end, mark_self, mark_tail


    def run(self, root):
        start = True
        self.imdcount = 0
        while start:
            self.imdcount += 1
            start, end, mark_self, mark_tail = self._walk(None, root, [], [], [], [])
            marked_tail = [x[0] for x in mark_tail]
            if start and end:
                for x in set(mark_self):
                    newelem = None
                    done = False
                    if x==start[0][0]:
                        before, after = x.text.split('[imd]',1)
                        x.text = before
                        label, imd = (None, after,) if '||' not in after.split('[/imd]')[0] else after.split('||',1)
                        newelem = self._wrap_in_span(imd)
                        x.insert(0, newelem)
                        if label:
                            newelem = self._wrap_in_span(label, 'label-imd-%s' % self.imdcount)
                            x.insert(0,newelem)
                        done = True
                    if x==end[0][0] and x not in marked_tail:
                        if newelem is not None:
                            x = newelem
                            before, after = x.text.split('[/imd]',1)
                            x.text = before
                            x.tail = after
                        else:
                            before, after = x.text.split('[/imd]',1)
                            n1 = self._wrap_in_span(before)
                            n2 = util.etree.Element('span')
                            n2.text = after
                            x.text = ''
                            x.insert(0,n1)
                            x.insert(1,n2)
                        done = True
                    if not done:
                        self._set_class(x)

                for pair in set(mark_tail):
                    x, parent = pair
                    newelem = None
                    done = False
                    if x==start[0][0] and x not in mark_self:
                        idx = parent.getchildren().index(x)

                        before, after = x.tail.split('[imd]',1)
                        label, imd = (None, after,) if '||' not in after.split('[/imd]')[0] else after.split('||',1)
                        n0 = None
                        if label:
                            n0 = self._wrap_in_span(label, 'label-imd-%s' % self.imdcount)
                        n1 = self._wrap_in_span(before, '')
                        n2 = self._wrap_in_span(imd)
                        x.tail = ''
                        parent.insert(idx+1, n2)
                        if n0 is not None:
                            parent.insert(idx+1,n0)
                        parent.insert(idx+1, n1)
                        newelem = n2
                        done = True
                    if x==end[0][0] and x in marked_tail:
                        if newelem is not None:
                            before, after = newelem.text.split('[/imd]',1)
                            newelem.text, newelem.tail = before, after
                        else:
                            before, after = x.tail.split('[/imd]',1)
                            x.tail = ''
                            n1 = self._wrap_in_span(before)
                            n2 = self._wrap_in_span(after, '')
                            idx = end[0][1].getchildren().index(x)
                            end[0][1].insert(idx+1, n2)
                            end[0][1].insert(idx+1, n1)
                        done = True
                    if not done:
                        n = self._wrap_in_span(x.tail)
                        parent.insert(parent.getchildren().index(x)+1, n)
                        x.tail = ''
                        
            else:
                if start:
                    s = start[0][0]
                    #print u'could not find end!', s.tag, s.text, u'|', s.tail
                    break
                if end:
                    e = end[0][0]
                    #print u'could not find start!', e.tag, e.text, u'|', e.tail
                    break

        return root

class InmoredetailExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.inlinePatterns.add('inmoredetail', InmoredetailPattern(IMD_RE), '_begin')
        md.treeprocessors.add('inmoredetial', InmoredetailTreeProcessor(), '_end')

def makeExtension(configs=[]):
    return InmoredetailExtension(Extension)
