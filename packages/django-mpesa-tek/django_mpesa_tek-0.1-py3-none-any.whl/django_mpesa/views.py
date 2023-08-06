from datetime import datetime
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from mpesa import api
from django_mpesa.models import Withdrawal, Deposit
from django_mpesa.serializers import (
    WithdrawalModelSerializer, DepositModelSerializer,
)
from pprint import pprint
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from time import sleep
import coreapi
import json
import pytz
import string
from django_mpesa import conf

# Create your views here.

if not hasattr(settings, 'MPESA_CONSUMER_KEY'):
    setattr(settings, 'MPESA_CONSUMER_KEY', conf.CONSUMER_KEY)
if not hasattr(settings, 'MPESA_CONSUMER_SECRET'):
    setattr(settings, 'MPESA_CONSUMER_SECRET', conf.CONSUMER_SECRET)
if not hasattr(settings, 'MPESA_ENV'):
    setattr(settings, 'MPESA_ENV', conf.MPESA_ENV)
if not hasattr(settings, 'MPESA_C2B_REF'):
    setattr(settings, 'MPESA_C2B_REF', conf.C2B_REF)
if not hasattr(settings, 'MPESA_B2C_REF'):
    setattr(settings, 'MPESA_B2C_REF', conf.B2C_REF)
if not hasattr(settings, 'MPESA_B2B_REF'):
    setattr(settings, 'MPESA_B2B_REF', conf.B2B_REF)
if not hasattr(settings, 'MPESA_C2B_SHORTCODE'):
    setattr(settings, 'MPESA_C2B_SHORTCODE', conf.SHORTCODE1)
if not hasattr(settings, 'MPESA_B2C_SHORTCODE'):
    setattr(settings, 'MPESA_B2C_SHORTCODE', conf.SHORTCODE2)
if not hasattr(settings, 'MPESA_BUSINESS_SHORTCODE'):
    setattr(settings, 'MPESA_BUSINESS_SHORTCODE', conf.BUSINESS_SHORTCODE)
if not hasattr(settings, 'MPESA_PASSCODE'):
    setattr(settings, 'MPESA_PASSCODE', conf.PASSCODE)
if not hasattr(settings, 'MPESA_TEST_MSISDN'):
    setattr(settings, 'MPESA_TEST_MSISDN', conf.TEST_MSISDN)

if not hasattr(settings, 'MPESA_RESULT_URL'):
    raise ImproperlyConfigured(
        "MPESA_RESULT_URL has not been defined in settings. Please do so.")
if not hasattr(settings, 'MPESA_CALLBACK_URL'):
    raise ImproperlyConfigured(
        "MPESA_CALLBACK_URL has not been defined in settings. Please do so.")
if not hasattr(settings, 'MPESA_TIMEOUT_URL'):
    raise ImproperlyConfigured(
        "MPESA_TIMEOUT_URL has not been defined in settings. Please do so.")
if not hasattr(settings, 'MPESA_CONFIRMATION_URL'):
    raise ImproperlyConfigured(
        "MPESA_CONFIRMATION_URL has not been defined in settings. Please do so.")
if not hasattr(settings, 'MPESA_VALIDATION_URL'):
    raise ImproperlyConfigured(
        "MPESA_VALIDATION_URL has not been defined in settings. Please do so.")

mpesa_env = settings.MPESA_ENV
app_key = settings.MPESA_CONSUMER_KEY
app_secret = settings.MPESA_CONSUMER_SECRET
mpesa_env = settings.MPESA_ENV


class B2CQueueTimeoutAPIView(CreateAPIView):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalModelSerializer
    permission_classes = [permissions.AllowAny, ]
    swaggger_schema = None

    def create(self, request):
        pprint(request.data)
        return Response({
            "ResultCode": 0
        })


class B2CResultAPIView(CreateAPIView):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalModelSerializer
    permission_classes = [permissions.AllowAny, ]
    swaggger_schema = None

    def create(self, request):
        """
        # ResultParameters below returned only if request was successful

        {
            "Result": {
                "ConversationId": "",
                "OriginatorConversationId": "",
                "ResultDesc": "",
                "ResultType": 0,
                "ResultCode": 0,
                "TransactionID": "",
                "ResultParameters": {
                    "ResultParameter": [
                        {"Key": "TransactionReceipt", "Value": "LXG21AA5TX"},
                        {"Key": "B2CWorkingAccountAvailableFunds", "Value": "2000.0"},
                        {"Key": "B2CUtilityAccountAvailableFunds",
                        "Value": "23654.5"},
                        {"Key": "TransactionCompletedDateTime",
                        "Value": "01.08.2018 16:12:12"},
                        {"Key": "ReceiverPublicPartyName",
                        "Value": "254722000000 - Safaricom PLC"},
                        {"Key": "B2CChargesPaidAccountAvailableFunds",
                        "Value": "236453.9"},
                        {"Key": "B2CRecipientIsRegisteredCustomer", "Value": "Y|N"},
                        {"Key": "TransactionAmount", "Value": 200},
                    ]
                }
            }
        }
        """
        pprint(request.data)
        rdata = request.data
        try:
            params = rdata.get("ResultParameters").get("ResultParameter")
            sdata = {d["Key"]: d["Value"] for d in params}
            pnumber = "+" + \
                sdata["ReceiverPublicPartyName"].split('-')[0].strip()
            name = sdata["ReceiverPublicPartyName"].split('-')[1].strip()
            amount = sdata["TransactionAmount"]
            transdate = datetime.strptime(
                sdata["TransactionCompletedDateTime"], "%d.%m.%Y %H:%M:%S")
            timezone = pytz.timezone("Africa/Nairobi")
            transdate = timezone.localize(transdate)
            PAYLOAD = {
                "ConversationId": rdata.get('ConversationId'),
                "OriginatorConversationId": rdata.get("OriginatorConversationId"),
                "ResultDesc": rdata.get("ResultDesc"),
                "ResultType": rdata.get("ResultType"),
                "ResultCode": rdata.get("ResultCode"),
                "MpesaReceiptNumber": rdata.get("TransactionID"),
                "Name": name,
                "Phonenumber": pnumber,
                "Amount": amount,
                "TransactionDateTime": transdate,
                "B2CRecipientIsRegisteredCustomer": sdata["B2CRecipientIsRegisteredCustomer"],
                "B2CChargesPaidAccountAvailableFunds": sdata["B2CChargesPaidAccountAvailableFunds"],
                "B2CWorkingAccountAvailableFunds": sdata["B2CWorkingAccountAvailableFunds"],
                "B2CUtilityAccountAvailableFunds": sdata["B2CUtilityAccountAvailableFunds"],
            }
            # PAYLOAD.update(sdata)
            ws = Withdrawal.objects.create(**PAYLOAD)
            ws.save()
            return Response({
                "ResultCode": 0
            })
        except:
            return Response({
                "ResultCode": 0
            })


class C2BConfirmationAPIView(CreateAPIView):
    """
    The payload from safaricom confirmation of c2b transaction.

    {
        "TransactionType":'Pay Bill',
        "TransID":"CSJDLASD",
        "TransTime":"20191120031623".
        "TransAmount":"270",
        "BusinessShortCode":"681445",
        "BillRefNumber":"29439",
        "InvoiceNumber":'',
        "OrgAccountBalance":"2300",
        "ThirdPartyTransID":'',
        "MSISDN":"254708374149",
        "FirstName":"John",
        "MiddleName":"J",
        "LastName":"Doe"
    }
    """
    queryset = Deposit.objects.all()
    serializer_class = DepositModelSerializer
    permission_classes = [permissions.AllowAny, ]
    swaggger_schema = None

    def create(self, request):
        payload = request.data
        pprint("Confirmation Payload")
        pprint(payload)
        fname = payload.get('FirstName')
        mname = payload.get('MiddleName')
        lname = payload.get('LastName')
        Phonenumber = "+"+str(payload.get("MSISDN"))
        pprint(Phonenumber)
        Amount = payload.get("TransAmount")
        TransactionDate = payload.get("TransTime")
        TransactionDateTime = datetime.strptime(
            str(TransactionDate), "%Y%m%d%H%M%S")
        timezone = pytz.timezone("Africa/Nairobi")
        TransactionDateTime = timezone.localize(TransactionDateTime)
        MDATA = {
            "TransactionType": payload.get("TransactionType"),
            "InvoiceNumber": payload.get("InvoiceNumber"),
            "BillRefNumber": payload.get("BillRefNumber"),
            "ThirdPartyTransID": payload.get("ThirdPartyTransID"),
            "Amount": payload.get("TransAmount"),
            "MpesaReceiptNumber": payload.get('TransID'),
            "Balance": payload.get('OrgAccountBalance'),
            "BusinessShortCode": payload.get('BusinessShortCode'),
            "TransactionDateTime": TransactionDateTime,
            "Phonenumber": "+"+str(payload.get("MSISDN")),
            "Name": fname+" "+mname+" "+lname,
        }
        pprint(MDATA)
        mdepo = Deposit.objects.create(**MDATA)
        mdepo.save()
        return Response({
            "ResultCode": 0
        })


class C2BValidationAPIView(CreateAPIView):
    """
    The payload from safaricom validation of c2b transaction.
    """
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalModelSerializer
    permission_classes = [permissions.AllowAny, ]
    swaggger_schema = None

    def create(self, request):
        payload = request.data
        pprint("Validation Payload")
        pprint(payload)
        return Response({
            "ResultCode": 0
        })


class LNMOnlineAPIView(CreateAPIView):
    """
    This is the payload received from  MPESA upon stk_push
    {
        'Body':{
            'stkCallback':{
                'MerchantRequestID':'199927-234475-1',
                'CheckoutRequestID':'ws_CO_DMZ_4016783493_8923u34y923u0',
                'ResultCode':0,
                'ResultDesc':'The service request is processed successfully.',
                'CallbackMetadata':{
                    'Item':[
                        {'Name':'Amount','Value':120.0},
                        {'Name':'MpesaReceiptNumber','Value':'NCVSJHSZS'},
                        {'Name':'Balance'},
                        {'Name':'TransactionDate','Value':'20191118180345'},
                        {'Name':'PhoneNumber','Value':'254741997729'}
                    ],
                }
            }
        }
    }
    """
    queryset = Deposit.objects.all()
    serializer_class = DepositModelSerializer
    permission_classes = [permissions.AllowAny, ]
    swaggger_schema = None

    def create(self, request):
        raw_data = request.data
        pprint(raw_data)
        stkcallback = raw_data["Body"]["stkCallback"]
        MerchantRequestID = stkcallback["MerchantRequestID"]
        CheckoutRequestID = stkcallback["CheckoutRequestID"]
        ResultCode = stkcallback["ResultCode"]
        ResultDesc = stkcallback["ResultDesc"]
        mditems = stkcallback["CallbackMetadata"]["Item"]
        xtract = {d.get('Name', ''): d.get('Value', '') for d in mditems}
        Amount = xtract["Amount"]
        MpesaReceiptNumber = xtract["MpesaReceiptNumber"]
        Balance = xtract["Balance"]
        TransactionDate = xtract["TransactionDate"]
        Phonenumber = "+"+str(xtract["PhoneNumber"])
        TransactionDateTime = datetime.strptime(
            str(TransactionDate), "%Y%m%d%H%M%S")
        timezone = pytz.timezone("Africa/Nairobi")
        TransactionDateTime = timezone.localize(TransactionDateTime)
        mydepo = Deposit.objects.create(
            MerchantRequestID=MerchantRequestID,
            CheckoutRequestID=CheckoutRequestID,
            ResultCode=ResultCode,
            ResultDesc=ResultDesc,
            Amount=Amount,
            MpesaReceiptNumber=MpesaReceiptNumber,
            Balance=Balance,
            TransactionDateTime=TransactionDateTime,
            Phonenumber=Phonenumber
        )
        mydepo.save()
        return Response({'status': 'Ok'})


def make_deposit(phonenumber, amount):
    PAYLOAD = {
        "amount": amount,
        "business_shortcode": settings.MPESA_BUSINESS_SHORTCODE,
        "callback_url": settings.MPESA_CALLBACK_URL,
        "description": "Deposit Funds",
        "passcode": settings.MPESA_PASSCODE,
        "phone_number": str(phonenumber),
        "reference_code": settings.MPESA_C2B_REF,
    }
    stk_push_user = api.mpesa_express.MpesaExpress(
        env=mpesa_env, app_key=app_key, app_secret=app_secret,
        sandbox_url='https://sandbox.safaricom.co.ke',
        live_url='https://api.safaricom.co.ke'
    )
    result = stk_push_user.stk_push(**PAYLOAD)
    return json.dumps(result)


def make_withdrawal(phonenumber, amount):

    PAYLOAD = {
        "amount": amount,
        "command_id": "BusinessPayment",
        "initiator_name": settings.MPESA_BUSINESS_SHORTCODE,
        "occasion": 'withdrawal_successful'
        "party_a": settings.MPESA_BUSINESS_SHORTCODE,
        "party_b": phonenumber,
        "queue_timeout_url": settings.MPESA_QUEUE_TIMEOUT_URL,
        "remarks": settings.MPESA_B2C_REF,
        "result_url": settings.MPESA_RESULT_URL,
        "security_credentials": settings.MPESA_SECURITY_CREDENTIALS,
        "transaction_id": get_random_string(16),
    }
    make_withdrawal = api.b2c.B2C(
        env=mpesa_env, app_key=app_key, app_secret=app_secret,
        sandbox_url='https://sandbox.safaricom.co.ke',
        live_url='https://api.safaricom.co.ke'
    )
    result = make_withdrawal.transact(**PAYLOAD)
    return json.dumps(result)


@permission_classes((IsAuthenticated,))
@api_view(['POST', ])
def do_mpesa_deposit(request):
    """
    Initiate Mpesa Customer Deposit for Kenya's *MPESA* System
    Post a *Kenya* *phonenumber* *+2547*  prefix
    Post {
        'phonenumber':'+243811545355',
        'amount':'4500',
    }
    to initiate b2c withdrawal.
    """
    if request.method == 'POST':
        phonenumber = request.data.get('phonenumber')
        amount = request.data.get('amount')
        res = make_deposit('+'+phonenumber, amount)
        return Response(res)


@permission_classes((IsAuthenticated,))
@api_view(['POST', ])
def do_mpesa_withdrawal(request):
    """
    Initiate Mpesa Customer Withdrawal for Kenya's *MPESA* System
    Post a *Kenya* *phonenumber* *+2547*  prefix
    Post {
            'phonenumber':'+243811545355',
            'amount':'4500',
    }
    to initiate b2c withdrawal.
    """
    if request.method == 'POST':
        phonenumber = request.data.get('phonenumber')
        amount = request.data.get('amount')
        res = make_withdrawal('+'+phonenumber, amount)
        return Response(res)


def register_my_urls():
    c2b_obj = api.c2b.C2B(
        env=settings.MPESA_ENV,
        app_key=app_key,
        app_secret=app_secret,
        sandbox_url='https://sandbox.safaricom.co.ke',
        live_url='https://api.safaricom.co.ke'
    )
    PAYLOAD = {
        "shortcode": settings.MPESA_C2B_SHORTCODE,
        "response_type": "Complete",
        "confirmation_url": settings.MPESA_CONFIRMATION_URL,
        "validation_url": settings.MPESA_VALIDATION_URL,
    }
    response = c2b_obj.register(**PAYLOAD)
    return json.dumps(response)
