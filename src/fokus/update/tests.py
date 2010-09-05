# -*- coding: utf8 -*-

from django.test import TestCase

from fokus.update.models import Update
from fokus.issue.models import Issue

class RecursionTest(TestCase):
    def setUp(self):
        self.base = Update.objects.create(text="Base update", content_type_id=0, object_id=0)
    
    def test_update_count(self):
        """
        Tests recursive update count.
        """
        LEVEL_COUNT = 10
        self.level1 = [Update.objects.create(parent=self.base, text="Level 1, update %d" % i) for i in range(LEVEL_COUNT)]
        
        print "Kjører rekursjonstest med %d updates på hvert nivå." % LEVEL_COUNT
        
        n = 0
        self.level2 = []
        for update in self.level1:
            self.level2 += [Update.objects.create(parent=update, text="Level 2, update %d" % (n * LEVEL_COUNT + i)) for i in range(LEVEL_COUNT)]
            n += 1
        
        print "Sjekker at antall barn av %s er lik %d" % (self.base, LEVEL_COUNT ** 2 + LEVEL_COUNT)
        self.assertEqual(self.base.get_child_count(), LEVEL_COUNT ** 2 + LEVEL_COUNT)
        
        print "Sjekker at antall oppdateringer tilknyttet %s er lik %d" % (self.base, LEVEL_COUNT ** 2 + LEVEL_COUNT + 1)
        self.assertEqual(self.base.get_update_count(), LEVEL_COUNT ** 2 + LEVEL_COUNT + 1)
    
    def test_ultimate_parent(self):
        # Dummy ultimate parent
        self.issue = Issue.objects.create(subject="Testsak", status_id=0, type_id=0)
        
        # Two levels of recursion
        self.level1 = Update.objects.create(parent=self.issue, text="Level 1")
        self.level2 = Update.objects.create(parent=self.level1, text="Level 2")
        
        # Perform ultimate parent assertions
        print "Sjekker at enhver etterkommer av en Issue får denne som issue-egenskap."
        self.assertEqual(self.level1.issue, self.issue)
        self.assertEqual(self.level2.issue, self.issue)

