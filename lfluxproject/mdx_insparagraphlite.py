from mdx_insparagraph import InsParagraphPreprocessor
import markdown

class InsParagraphProcessor(markdown.treeprocessors.Treeprocessor):
    """ Process Paragraph blocks. """

    def run(self, root):
        for child in root:
            if child.tag=='ins':
                continue
            if (child.text or '').lstrip().startswith('.ins'):
                newelem = markdown.util.etree.Element('span')
                newelem.text = root.text.lstrip()[5:]
                children = list(root.getchildren())
                for child2 in children:
                    newelem.append(child2)
                    root.remove(child2)
                child.text = ''
                child.insert(0, newelem)
            else:
                self.run(child)
        return root

class InsparagraphLiteExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.treeprocessors['insparagraph'] = InsParagraphProcessor(md)
        md.preprocessors.insert(0, 'insparagraph',
                                InsParagraphPreprocessor(md))
        

def makeExtension(configs=[]):
    return InsparagraphLiteExtension()
