from django.contrib import admin
from . import models

admin.site.register(models.Clients)
admin.site.register(models.Invoices)
admin.site.register(models.Payments)
