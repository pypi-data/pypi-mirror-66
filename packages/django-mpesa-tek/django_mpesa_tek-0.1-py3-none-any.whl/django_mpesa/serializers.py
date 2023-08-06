from rest_framework import serializers
from django_mpesa.models import Deposit, Withdrawal, VodacashCallback


class DepositModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['id', 'MpesaReceiptNumber', 'TransactionDateTime', 'Amount', 'Phonenumber',
                  'MerchantRequestID', 'CheckoutRequestID', 'Balance', 'ResultCode', 'ResultDesc']


class WithdrawalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = '__all__'
        exclude_fields = 'created_at'
