from pygsuite.constants import CLIENTS
from pygsuite.docs.body import Body
from pygsuite.utility.decorators import safe_property

class Document():
    def __init__(self, id = None, name = None, service = None, _document=None):
        service = service or CLIENTS.docs_client
        self.service = service
        self.id = id
        self._document = _document or service.documents().get(documentId=id).execute()
        self._change_queue = []

    def id(self):
        return self._document['id']

    def flush(self):
        out = self.service.documents().batchUpdate(body={'requests': self._change_queue},
                                                       documentId=self.id).execute()['replies']
        self._change_queue = []
        self.refresh()
        return out

    @property
    def body(self):
        return Body(self._document.get('body'), self._document)

    @property
    def footers(self):
        return [Worksheet(item, self._sheet) for item in self._sheet.worksheets()]

    @property
    def footnotes(self):
        return [Worksheet(item, self._sheet) for item in self._sheet.worksheets()]

    @property
    def headers(self):
        return [Worksheet(item, self._sheet) for item in self._sheet.worksheets()]

    @property
    def title(self):
        return self._document.get('title')

    @title.setter
    def title(self, x):
        raise NotImplementedError

    def refresh(self):
        self._sheet = self.service.documents().get(documentId=id).execute()
