from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('registerphone/', RegisterPhoneView.as_view(),
         name='register_phone_number'),
    path('logout/', LogoutView.as_view(),
         name='logout'),
    path('login/password/', LoginUsingPassword.as_view(),
         name='login'),
    path('verifyotp/', OtpView.as_view(), name='verify_otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/update/', UpdateData.as_view(), name='verify_otp'),
    path('email/confirm/', EmailConfView.as_view(), name='verification_token'),
    path('address/', AddressView.as_view(), name='address'),
    path('address/<str:AIDINSTANCE>/',
         AddressInstance.as_view(), name='address instance'),
    path('phone/', PhoneNumberView.as_view(), name='phone number'),
    path('pincode/', PincodeNumberView.as_view(), name='pincode'),
    path('phone/<str:PHIDINSTANCE>/', PhoneNumberInstanceView.as_view(),
         name='phone number instance'),
    path('pincode/<str:PCIDINSTANCE>/',
         PincodeNumberInstanceView.as_view(), name='pincode number instance'),
    path('password/change/',
         PasswordChangeRequestView.as_view(), name='password change view'),
    path('password/change/confirm/<str:verif_token>/',
         PasswordChangeRequestConfirmationView.as_view(), name='password change view confirm'),
    #     path('verify/phone/instance/',
    #          VerifyPhoneForInstanceView.as_view(), name='verify instance'),
    #     path('verify/phone/instance/token/',
    #          CheckInstanceTokenView.as_view(), name='instance token verification'),
    path('phone/verify/otp/',
         OtpInstanceGenrator.as_view(), name='otp instance'),
    path('password/set/',
         SetPasswordChangeRequestConfirmationView.as_view(), name='set password change view confirm'),
    path('profile/get/',
         ProfileData.as_view(), name='profile data'),
    path('fmc/add/',
         fmctokenview.as_view(), name='fmc')

]
