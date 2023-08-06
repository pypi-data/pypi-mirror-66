from django.urls import path
from django.conf.urls import include
from django_mpesa import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('stk_push_callback', views.LNMOnlineAPIView,
                basename='stk_push_callback')
router.register('confirmation_url', views.C2BConfirmationAPIView,
                basename='confirmation_url')
router.register('validation_url', views.C2BValidationAPIView,
                basename='validation_url')
router.register('result_url', views.B2CResultAPIView, basename='result_url')
router.register('queue_timeout_url', views.B2CQueueTimeoutAPIView,
                basename='queue_timeout_url')

url_patterns = [
    path('', include(router.urls)),
    path('trigger_mpesa_stk_payment/', views.do_mpesa_deposit,
         name="trigger_mpesa_stk_payment"),
    path('do_mpesa_b2c_payment/', views.do_mpesa_withdrawal,
         name="do_mpesa_b2c_payment"),
]
