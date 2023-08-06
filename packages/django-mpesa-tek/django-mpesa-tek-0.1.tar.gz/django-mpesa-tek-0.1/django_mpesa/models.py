from django.db import models
# Create your models here.


class Withdrawal(models.Model):
    ConversationId = models.CharField(max_length=50, blank=True, null=True)
    OriginatorConversationId = models.CharField(
        max_length=50, blank=True, null=True)
    ResultDesc = models.CharField(max_length=50, blank=True, null=True)
    ResultType = models.IntegerField(null=True, blank=True)
    ResultCode = models.IntegerField(null=True, blank=True)
    MpesaReceiptNumber = models.CharField(max_length=50, blank=True, null=True)
    Name = models.CharField(max_length=86, null=True, blank=True)
    Phonenumber = models.CharField(max_length=50, blank=True, null=True)
    Amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    TransactionDateTime = models.DateTimeField(blank=True, null=True)
    B2CRecipientIsRegisteredCustomer = models.CharField(
        max_length=50, null=True, blank=True)
    B2CChargesPaidAccountAvailableFunds = models.DecimalField(
        max_digits=50, decimal_places=2, default=0)
    B2CWorkingAccountAvailableFunds = models.DecimalField(
        max_digits=50, decimal_places=2, default=0)
    B2CUtilityAccountAvailableFunds = models.DecimalField(
        max_digits=50, decimal_places=2, default=0)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.MpesaReceiptNumber + " "+self.Phonenumber + " " + str(self.Amount)


class Deposit(models.Model):
    MerchantRequestID = models.CharField(max_length=56, blank=True, null=True)
    CheckoutRequestID = models.CharField(max_length=46, blank=True, null=True)
    ResultCode = models.IntegerField(default=0)
    ResultDesc = models.CharField(max_length=86, blank=True, null=True)
    Amount = models.DecimalField(max_digits=13, decimal_places=2, default=0.0)
    MpesaReceiptNumber = models.CharField(max_length=26, blank=True, null=True)
    Balance = models.CharField(max_length=16, blank=True, null=True)
    TransactionDateTime = models.DateTimeField(blank=True, null=True)
    Phonenumber = models.CharField(max_length=44, blank=True, null=True)
    Name = models.CharField(max_length=56, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.MpesaReceiptNumber + " "+self.Phonenumber + " " + str(self.Amount)

    class Meta:
        ordering = ('-TransactionDateTime',)
