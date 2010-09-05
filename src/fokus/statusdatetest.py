#!/usr/bin/env python

from economy.invoices.models import *
import datetime

change = Change.objects.all()[0]
change.status = ChangeStatus.objects.all()[0]
sd = change.status_date()
sd.date = sd.date - datetime.timedelta(days=10)
print "Endret dato til %s" % sd.date
sd.save()

print change.status_date()
