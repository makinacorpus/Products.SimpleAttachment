from Products.CMFCore.utils import getToolByName
from logging import getLogger

from zope.interface import implements
from ZODB.POSException import ConflictError

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.file import ATFile
from Products.Archetypes.public import registerType
from Products.SimpleAttachment.config import PROJECTNAME
from Products.SimpleAttachment.interfaces import IFileAttachment

debug = getLogger(__name__).debug
schema = ATFile.schema.copy()


class FileAttachment(ATFile):
    """A file attachment"""

    implements(IFileAttachment)

    portal_type = meta_type = 'FileAttachment'
    schema = schema
    security = ClassSecurityInfo()

    security.declarePrivate('getIndexValue')
    def getIndexValue(self, mimetype='text/plain'):
        """Copy/paste from plone.app.blob
        """
        field = self.getPrimaryField()
        source = field.getContentType(self)
        transforms = getToolByName(self, 'portal_transforms')
        if transforms._findPath(source, mimetype) is None:
            return ''
        value = str(field.get(self))
        filename = field.getFilename(self)
        try:
            return str(transforms.convertTo(mimetype, value,
                mimetype=source, filename=filename))
        except (ConflictError, KeyboardInterrupt):
            raise
        except:
            getLogger(__name__).exception('exception while trying to convert '
               'blob contents to "text/plain" for %r', self)

registerType(FileAttachment, PROJECTNAME)
