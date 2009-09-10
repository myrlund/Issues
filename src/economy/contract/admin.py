from django.contrib import admin
from economy.contract.models import Contract, ContractCategory, Project

class ContractAdmin(admin.ModelAdmin):
    list_display = ("code", "project", "company", "amount",)
    list_filter = ("project",)
    ordering = ("project", "code",)

admin.site.register(Contract, ContractAdmin)
admin.site.register(ContractCategory)
admin.site.register(Project)
