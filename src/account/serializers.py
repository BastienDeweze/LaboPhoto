from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from .models import CustomUser, ForgotCode
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

UserModel = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):

    re_password = serializers.CharField()

    class Meta:
        model = UserModel
        fields = ('id', 'email', 'password', 're_password')
        extra_kwargs = {'password': {'write_only': True}, 're_password': {'write_only': True}}

    def create(self, validated_data):
        user = UserModel.objects.create_user(validated_data['email'], validated_data['password'])
        return user

    def validate(self, data):
        re_password = data.get('re_password')
        password = data.get('password')
        
        if password == re_password :
            return data
        else :
            raise serializers.ValidationError(detail={'PasswordNotMatch': 'Mot de passe non correspondant'})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'email', "is_confirm")


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        
        if not user :
            raise serializers.ValidationError(detail={'NotFound': 'User not found'})
        elif not user.is_confirm :
            raise serializers.ValidationError(detail={'NotActif': ''})
        elif user and user.is_active:
            return user

class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField()
    re_password = serializers.CharField()

    class Meta:
        extra_kwargs = {'password': {'write_only': True}, 're_password': {'write_only': True}}

    def validate(self, data):

        email = data.get('email')
        password = data.get('password')
        re_password = data.get('re_password')

        user = CustomUser.objects.filter(email=email)
        
        if user.exists() :
            user = user[0]
            if password == re_password:
                data['user'] = user
                return data
            else :
                raise serializers.ValidationError(detail={'ForgotError': "Mot de passe non-correspondant"})
        else :
            raise serializers.ValidationError(detail={'ForgotError': "Cette utilisateur n'existe pas"})


class ActiveAccountSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        code = data.get('code')
        email = data.get('email')

        user = CustomUser.objects.filter(email=email)
        if user.exists() and not user[0].is_confirm :
            code_user = user[0].code

            if len(code) == 6 and code.isdigit() and str(code_user) == code :
                data['user'] = user[0]
                return data

            else :
                msg = _("Code invalide !")
                raise serializers.ValidationError(detail={'CodeError': 'Code invalide !'})
        
        else :
            msg = _("Erreur user !")
            raise serializers.ValidationError(detail={'CodeError': 'Erreur user !'})
            

class ForgotConfirmSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        code = data.get('code')
        email = data.get('email')
        print("in ser")
        user = CustomUser.objects.filter(email=email)
        
        if user.exists() :
            code_user = ForgotCode.objects.filter(user_id=user[0].pk)
            if code_user.exists() :
                code_user = code_user[0]
                if code_user.is_valid():

                    if len(code) == 6 and code.isdigit() and str(code_user) == code:
                        data['user'] = user[0]
                        return data

                    else :
                        raise serializers.ValidationError(detail={'ForgotCodeError': 'Code invalide !'})
                
                else :
                    raise serializers.ValidationError(detail={'ForgotCodeError': 'Ce code à déja été utilisé ou à expiré'})
            else :
                raise serializers.ValidationError(detail={'ForgotCodeError': 'Respectez les étatpes.'})
        
        else :
            raise serializers.ValidationError(detail={'ForgotCodeError': 'Erreur user !'})