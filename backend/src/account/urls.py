from django.urls import path
from .views import RegistrationAPI, UserAPI, LoginView, SendConfirmMail, ConfirmView, Me, LogoutAPI, ForgotView, ChangePasswordView
from knox import views as knox_views

urlpatterns = [
    path('register/', RegistrationAPI.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('user/<int:pk>', UserAPI.as_view(), name="user"),
    path('me/', Me.as_view(), name="user"),
    path('logout/', LogoutAPI.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('sendconfirm/<int:pk>', SendConfirmMail.as_view(), name='sendconfirm'),
    path('confirm/', ConfirmView.as_view(), name='confirm'),
    path('forgot/', ForgotView.as_view(), name='forgot'),
    path('confirmforgot/', ChangePasswordView.as_view(), name='confirmforgot'),
    
]