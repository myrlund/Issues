from django.test import TestCase

from fokus.issue.models import Issue
from fokus.attachment.models import Attachment, AttachmentType, FileExtension

class AttachmentTest(TestCase):
    def setUp(self):
        self.issue = Issue.objects.create(subject="Attachable issue", status_id=0, type_id=0)
        
        self.image_type = AttachmentType.objects.create(name="image", title="Bilder")
        self.document_type = AttachmentType.objects.create(name="documents", title="Dokumenter")
        self.other_type = AttachmentType.objects.create(name="other", title="Annet")
        AttachmentType.default = self.other_type
        
        FileExtension.objects.create(extension="txt", type=self.document_type)
        FileExtension.objects.create(extension="pdf", type=self.document_type)
        FileExtension.objects.create(extension="xls", type=self.document_type)
        FileExtension.objects.create(extension="doc", type=self.document_type)
        FileExtension.objects.create(extension="jpg", type=self.image_type)
        FileExtension.objects.create(extension="png", type=self.image_type)
        FileExtension.objects.create(extension="tiff", type=self.image_type)
    
    def test_auto_fields(self):
        """
        Tests that attachment field auto-generation work as expected.
        """
        txt = Attachment.objects.create(file="foobar.txt", parent=self.issue)
        self.assertEqual(self.document_type, txt.type)
        
        jpg = Attachment.objects.create(file="DSC001.JPG", parent=self.issue)
        self.assertEqual(self.image_type, jpg.type)
        
        unknown = Attachment.objects.create(file="kryptisk.hqx", parent=self.issue)
        self.assertEqual(self.other_type, unknown.type)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

