## -*- coding: utf8 -*-
#
#from django.test import TestCase
#from datetime import datetime
#
#from fokus.contract.models import ContractCategory, Contract, Project
#from fokus.invoices.models import Invoice
#
#class DeleteTest(TestCase):
#    def setUp(self):
#        now = datetime.now()
#        
#        self.project = Project.objects.create(number=666, title="Testprosjekt")
#        self.cat = ContractCategory.objects.create(title="Testkategori")
#        self.contracts = [
#            Contract.objects.create(project=self.project, category=self.cat, code="TEST01"),
#            Contract.objects.create(project=self.project, category=self.cat, code="TEST02"),
#            Contract.objects.create(project=self.project, category=self.cat, code="TEST03"),
#        ]
#        self.invoices = {}
#        for contract in self.contracts:
#            self.invoices[contract] = [
#                Invoice.objects.create(contract=contract, description="Faktura nr. 1", number=1, date=now),
#                Invoice.objects.create(contract=contract, description="Faktura nr. 2", number=2, date=now),
#            ]
#    
#    def test_simple_delete(self):
#        """
#        Tester enkel delete
#        """
#        count = len(self.contracts)
#        self.contracts[0].delete()
#        newcount = len(Contract.objects.all())
#        self.failUnlessEqual(count - 1, newcount, "Klarte ikke å slette kontrakt.")
#        self.cat = ContractCategory.objects.all()[0]
#        print "All:", self.cat.contract_set.all()
#        newcount = len(self.cat.contract_set.all())
#        self.failUnlessEqual(count - 1, newcount, "Slettet kontrakt dukker fortsatt opp i foreign qs.")
#        
#        
#        
#        # 
