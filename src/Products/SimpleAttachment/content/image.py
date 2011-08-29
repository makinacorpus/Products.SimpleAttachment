from zope.interface import implements

from Products.ATContentTypes.content.image import ATImage
from Products.Archetypes.public import registerType

from Products.SimpleAttachment.config import PROJECTNAME
from Products.SimpleAttachment.interfaces import IImageAttachment


class ImageAttachment(ATImage):
    """An image attachment"""

    implements(IImageAttachment)

    portal_type = meta_type = 'ImageAttachment'

    def index_html(self, REQUEST, RESPONSE):
        """ download the file inline or as an attachment """
        field = self.getPrimaryField()
        return field.index_html(self, REQUEST, RESPONSE)

registerType(ImageAttachment, PROJECTNAME)
