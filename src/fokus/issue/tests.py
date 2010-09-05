from datetime import datetime

from django.test import TestCase

from fokus.issue.models import Issue, IssueStatus, IssueType, Project, Contract
from django.contrib.auth.models import User

class IssueTest(TestCase):
    STATUS_TITLES = (
        (1, "Ny"),
        (2, "Behandles"),
        (3, "Lukket"),
    )
    
    def setUp(self):
        self.project = Project.objects.create(title="Testprosjekt", number=666)
        self.contract = Contract.objects.create(company="Testselskap", code=666, project=self.project)
        
        self.statuses = [IssueStatus.objects.create(name=title.lower(), title=title, weight=weight) for (weight, title) in self.STATUS_TITLES]
        self.type = IssueType.objects.create(title="Testtype")
    
    def test_upload_path_generation(self):
        """
        Tests upload file path generation goes as expected.
        """
        issue = Issue.objects.create(subject="Testsak", type=self.type)
        
        filename = "foo.txt"
        now = datetime.now()
        
        path = issue.get_upload_path(filename)
        expected = "%s/0/%s-%s" % (issue.id, now.strftime("%Y-%m-%d-%H%M"), filename)
        
        print "Sjekker at Issue genererer korrekt filsti: %s" % path
        self.assertEqual(expected, path)

    def test_get_issues(self):
        user = User.objects.create(username="testuser")
        
        dummy_contract = Contract.objects.create(code=199, project=self.project, company="Eoh")
        dummy_issue = Issue.objects.create(subject="Dummy issue", type=self.type)
        dummy_issue.contracts.add(dummy_contract)
        dummy_issue.responsible.add(user)
        
        user_issue = Issue.objects.create(subject="User issue", type=self.type)
        user_issue.responsible.add(user)
        user_issue.contracts.add(self.contract)
        
        self.assertEqual(len(self.project.get_all_issues()), 2)
        self.assertEqual(len(self.project.get_all_issues(user)), 2)
        self.assertEqual(len(self.contract.get_all_issues()), 1)
        self.assertEqual(len(self.contract.get_all_issues(user)), 1)
        
        loose_issue = Issue.objects.create(subject="Other", type=self.type)
        loose_issue.contracts.add(self.contract)
        
        self.assertEqual(len(self.project.get_all_issues()), 3)
        self.assertEqual(len(self.project.get_all_issues(user)), 2)
        self.assertEqual(len(self.contract.get_all_issues()), 2)
        self.assertEqual(len(self.contract.get_all_issues(user)), 1)
        
        self.assertEqual(self.project.get_all_issues(user)[0], user_issue)
        self.assertEqual((self.project.get_all_issues() & self.project.get_all_issues(user))[0], user_issue)

