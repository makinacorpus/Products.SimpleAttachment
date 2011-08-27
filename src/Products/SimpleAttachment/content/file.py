from copy import deepcopy
from logging import getLogger
from zope.annotation.interfaces import IAnnotations
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View
from Products.ATContentTypes.content.file import ATFile
from Products.Archetypes.public import registerType, FileField
from Products.SimpleAttachment.config import PROJECTNAME

debug = getLogger(__name__).debug
key = 'transforms_cache'


class CachingFileField(FileField):
    """Version of AT's file field, which used to add a transform cache.
    """

    def set(self, instance, value, **kwargs):
        annotations = IAnnotations(instance)
        if key in annotations:
            del annotations[key]
        return super(CachingFileField, self).set(instance, value, **kwargs)


def makeField(field):
    """ mostly copied from `Archetypes.Field.Field.copy` """
    cdict = dict(vars(field))
    cdict.pop('__name__')
    # Widget must be copied separatedly
    widget = cdict['widget']
    del cdict['widget']
    properties = deepcopy(cdict)
    properties['widget'] = widget.copy()
    return CachingFileField(field.getName(), **properties)


schema = ATFile.schema.copy()
schema['file'] = makeField(schema['file'])
schema['file'].index_method = 'indexData'


class FileAttachment(ATFile):
    """A file attachment"""

    portal_type = meta_type = 'FileAttachment'
    schema = schema
    security = ClassSecurityInfo()

    security.declareProtected(View, 'indexData')
    def indexData(self, mimetype=None):
        """ index accessor """
        if not mimetype == 'text/plain':
            return self.getFile()
        return self.getField('file').getIndexable(self)

    def setFile(self, value):
        """ wrapper for "file" field mutator with cache invalidation """
        annotations = IAnnotations(self)
        if key in annotations:
            del annotations[key]
        return super(FileAttachment, self).setFile(value)


registerType(FileAttachment, PROJECTNAME)
