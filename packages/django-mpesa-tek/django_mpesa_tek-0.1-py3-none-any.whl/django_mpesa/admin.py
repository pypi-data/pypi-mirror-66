from django.contrib import admin
from django_mpesa.models import Deposit, Withdrawal

# Register your models here.


class WlAdmin(admin.ModelAdmin):
    model = Withdrawal
    date_hierarchy = 'created_at'
    list_display = [
        "TransactionDateTime",
        "MpesaReceiptNumber",
        "Phonenumber",
        "Amount",
        "B2CWorkingAccountAvailableFunds",
        "Name",
    ]
    search_fields = [
        "TransactionDateTime",
        "MpesaReceiptNumber",
        "Phonenumber",
        "Amount",
        "Name",
    ]


class DpAdmin(admin.ModelAdmin):
    model = Deposit
    date_hierarchy = 'created_at'
    list_display = [
        "TransactionDateTime",
        "MpesaReceiptNumber",
        "Phonenumber",
        "Amount",
        "Balance",
        "Name",
        "CheckoutRequestID"
    ]
    search_fields = [
        "TransactionDateTime",
        "MpesaReceiptNumber",
        "Phonenumber",
        "Amount",
        "Name",
        "CheckoutRequestID"
    ]


admin.site.register(Deposit, DpAdmin)
admin.site.register(Withdrawal, WlAdmin)
