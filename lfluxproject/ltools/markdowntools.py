import markdown
import markdown.util
import copy
import re



def monkeypatch_markdown_ins_and_del_are_not_blocklevel_elements():
    BLOCK_LEVEL_ELEMENTS = re.compile("^(p|div|h[1-6]|blockquote|pre|table|dl|ol|ul"
                                      "|script|noscript|form|fieldset|iframe|math"
                                      "|ins|del|hr|hr/|style|li|dt|dd|thead|tbody"
                                      "|tr|th|td|section|footer|header|group|figure"
                                      "|figcaption|aside|article|canvas|output"
                                      "|progress|video)$".replace('ins|del|',''))

    markdown.util.BLOCK_LEVEL_ELEMENTS = BLOCK_LEVEL_ELEMENTS

monkeypatch_markdown_ins_and_del_are_not_blocklevel_elements()


def pars_to_blocks(pars):
    pars = list(pars)
    m = markdown.Markdown()
    bp = markdown.blockprocessors.build_block_parser(m)

    root = markdown.util.etree.Element('div')

    blocks = []

    while pars:
        parsbefore = list(pars)
        for processor in bp.blockprocessors.values():
            if processor.test(root, pars[0]):
                processor.run(root, pars)

                while len(parsbefore) > len(pars):
                    blocks.append(parsbefore[0])
                    parsbefore = parsbefore[1:]

                if pars and pars[0].strip('\n') != parsbefore[0].strip('\n'):
                    pb0s = parsbefore[0].strip('\n')
                    p0s = pars[0].strip('\n')
                    if pb0s.endswith(p0s):
                        lpb = len(pb0s)
                        lp = len(p0s)
                        b = pb0s[0:lpb-lp]
                        blocks.append(b)

                    else:
                        raise Exception('unsupported change by blockprocessor. abort! abort!')

                break
    return blocks

