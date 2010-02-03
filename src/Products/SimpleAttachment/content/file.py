from zope.annotation.interfaces import IAnnotations
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View
from Products.ATContentTypes.content.file import ATFile
from Products.Archetypes.public import registerType


schema = ATFile.schema.copy()
schema['file'].index_method = 'indexData'


class FileAttachment(ATFile):
    """A file attachment"""

    portal_type = meta_type = 'FileAttachment'
    schema = schema
    key = 'transforms_cache'
    security = ClassSecurityInfo()

    security.declareProtected(View, 'indexData')
    def indexData(self, mimetype=None):
        """ index accessor with caching of the result """
        if not mimetype == 'text/plain':
            return self.getFile()
        annotations = IAnnotations(self)
        if self.key in annotations:
            value = annotations[self.key]
        else:
            text = self.getField('file').getIndexable(self)
            value = annotations[self.key] = text
        return value

    def setFile(self, value):
        """ wrapper for "file" field mutator with cache invalidation """
        annotations = IAnnotations(self)
        if self.key in annotations:
            del annotations[self.key]
        return super(FileAttachment, self).setFile(value)


registerType(FileAttachment)
