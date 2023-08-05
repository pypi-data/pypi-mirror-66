from dataclasses import dataclass
from typing import List, Dict

from .paragraph_elements import AutoText, ColumnBreak, HorizontalRule, PageBreak, TextRun, FootnoteReference, Equation

# from .doc_elements.image import Image
class ParagraphElement(object):
    def __init__(self, element, document):
        self._element = element
        self._document = document

    def __new__(cls, element, document):
        if element.get('autoText'):
            return AutoText(element, document)
        elif element.get('textRun'):
            return TextRun(element, document)
        elif element.get('ColumnBreak'):
            return ColumnBreak(element, document)
        elif element.get('HorizontalRule'):
            return HorizontalRule(element, document)
        elif element.get('PageBreak'):
            return PageBreak(element, document)
        elif element.get('FootnoteReference'):
            return FootnoteReference(element, document)
        elif element.get('Equation'):
            return Equation(element, document)


class Paragraph(object):
    def __init__(self, element, document):
        self._element = element
        self._document = document
        self._paragraph = self._element.get('paragraph')

    def end_index(self):
        return self._element.get('endIndex')

    def start_index(self):
        return self._element.get('startIndex')

    @property
    def elements(self):
        return [ParagraphElement(elem, self._document) for elem in self._paragraph.get('elements')]

    @property
    def text(self):
        return ''.join([element.content for element in self.elements if isinstance(element, TextRun)])
#

