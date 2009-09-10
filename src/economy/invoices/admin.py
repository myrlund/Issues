
from economy.invoices.models import *
from django.contrib import admin

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("project", "contract", "invoice_number", "invoice_date",)
    list_filter = ("contract",)
    ordering = ("-invoice_date", "contract", "-invoice_number",)

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Change)
admin.site.register(ChangeStatus)
