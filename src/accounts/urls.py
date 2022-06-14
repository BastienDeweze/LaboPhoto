from django.urls import path
from .views import SignUpView, Login, Logout, DetailAccount
from django.contrib.auth.decorators import login_required


app_name = 'account'

urlpatterns = [
    path('', login_required(DetailAccount.as_view(), login_url='account:login'), name="profile"),
    path('register/', SignUpView.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', login_required(Logout.as_view(), login_url='account:login'), name="logout"),
]