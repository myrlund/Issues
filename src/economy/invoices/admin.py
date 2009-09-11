
from economy.invoices.models import *
from django.contrib import admin

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("project", "contract", "number", "date",)
    list_filter = ("contract",)
    ordering = ("-date", "contract", "-number",)

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Change)
admin.site.register(ChangeStatus)
