from django.shortcuts import render
from rest_framework import permissions, generics
from rest_framework.response import Response
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer, ActiveAccountSerializer, ForgotPasswordSerializer, ForgotConfirmSerializer
from django.contrib.auth import login, logout
from .models import CustomUser, ForgotCode
from rest_framework import status
from .auth import TokenAuthSupportCookie
from datetime import datetime
import dateutil.parser
from laboPhoto.customPermissions import IsMe

from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView

# Verification email
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # send mail
        return Response({
            "NotActif": "Compte à confirmer",
        })

class SendConfirmMail(generics.GenericAPIView):
    
    mail_subject = 'Code de vérification'
    mail_templates = 'loginCode.html'

    def post(self, request, *args, **kwargs):
        print(kwargs["pk"])
        user = CustomUser.objects.get(pk=kwargs["pk"])
        if user :
            mail_subject = self.mail_subject
            message = render_to_string(self.mail_templates, {
                'user': user,
                'code': user.code,
            })
            to_email = user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return Response({ 'success': 'Mail envoyé !' })

        else :
            return Response({ 'error': 'Premier facteur non-effectué !' })


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        print(request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data
        login(request, user)
        response = super(LoginView, self).post(request, format=None)

        token = response.data['token']
        # return response.data['token']
        del response.data['token']

        date_time_obj = dateutil.parser.parse(response.data['expiry'])
        expires = datetime.strftime(date_time_obj, "%a, %d-%b-%Y %H:%M:%S GMT")

        response.set_cookie(
            'auth_token',
            token,
            expires = expires,
            httponly = True,
            samesite = 'strict'
        )

        return response

class LogoutAPI(KnoxLogoutView):
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = (TokenAuthSupportCookie,)

    def post(self, request, format=None):


        logout(request)
        
        print(request.COOKIES)
        response =  super(LogoutAPI, self).post(request, format=None)

        response.delete_cookie('auth_token')
        response.delete_cookie('csrftoken')

        return response

class ConfirmView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ActiveAccountSerializer

    def post(self, request, format=None):
        serializer = ActiveAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.get(email=serializer.validated_data["email"])
        user.is_confirm = True
        user.save()
        
        login(request, user)
        response = super(ConfirmView, self).post(request, format=None)

        token = response.data['token']
        # return response.data['token']
        del response.data['token']

        response.set_cookie(
            'auth_token',
            token,
            httponly = True,
            samesite = 'strict'
        )

        return response

class UserAPI(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsMe, ]
    serializer_class = UserSerializer

    # def get_object(self):
    #     return self.request.user

class Me(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        print(self.request.COOKIES)
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        topProfile = user.topprofiledata
        profileData = user.profiledata
        textData = user.textdata 
        
        is_valid = True if topProfile.isValid and profileData.isValid and textData.isValid else False
        
        return Response({ 'id': user.id, 'email': user.email,'is_confirm': user.is_confirm,'is_valid': is_valid})


class ForgotView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        new_password = serializer.validated_data['password']
        userForgot = ForgotCode.objects.filter(user=user)

        if userForgot.exists():
            userForgot.delete()

        ForgotCode.objects.create(user=user, new_password=new_password)
        
        return Response({ 'SuccessForgot': 'user.forgotcode.expiry' })


class ForgotConfirmView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        user.forgotcode.setConfirmationDate()
        user.forgotcode.save()

        return Response({ 'success': user.forgotcode.confirmationDate })


class ChangePasswordView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = ForgotConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("pre view")
        user = serializer.validated_data['user']
        new_password = user.forgotcode.new_password
        user.set_password(new_password)
        user.forgotcode.delete()
        user.save()
        print(user.password)
        return Response({ 'ChangeSuccess': "mot de passe changé avec succes" })