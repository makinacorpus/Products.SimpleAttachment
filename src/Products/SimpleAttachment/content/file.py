from logging import getLogger
from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.file import ATFile
from Products.Archetypes.public import registerType
from Products.SimpleAttachment.config import PROJECTNAME

debug = getLogger(__name__).debug


schema = ATFile.schema.copy()


class FileAttachment(ATFile):
    """A file attachment"""

    portal_type = meta_type = 'FileAttachment'
    schema = schema
    security = ClassSecurityInfo()


registerType(FileAttachment, PROJECTNAME)
