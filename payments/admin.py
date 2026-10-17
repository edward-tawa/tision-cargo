from django.contrib import admin
from .models.payment_models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "driver", "amount", "currency", "status", "created_at")
    list_filter = ("status", "currency", "created_at")
    search_fields = ("ecocash_number", "client_correlator", "correlator_id", "driver__username")
