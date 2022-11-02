from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 

from account.models import PmsUser, PmsUserDetails
from account import utils
from common_utils.reset_email_pass import Util
# class PmsTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token["is_active"] = user.is_superuser
#         token["is_active"] = user.is_active
#         return token        

class PmsTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return {
            "username": self.user.username,
            "email": self.user.email,
            "permissions": self.user.user_permissions.values_list("codename", flat=True),
            "groups": self.user.groups.values_list("name", flat=True),
            **attrs,
        }


class PmsUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsUser
        fields = [
            "id",
            "email",
            "first_name",
        ]


class PmsUserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, allow_null=False, allow_blank=False)
    password = serializers.CharField(max_length=255,
                                    style={'input_type':True},
                                    write_only=True)
    first_name =serializers.CharField(max_length=255)
    last_name =serializers.CharField(max_length=255)
    
    class Meta:
        model = PmsUser
        fields = tuple(PmsUser.REQUIRED_FIELDS) + (
            "id",
            "password",
            "email",
        )
   
    def create(self, validated_data):
        with transaction.atomic():
           
            user = PmsUser.objects.create_user(**validated_data)
            user.is_active = True
            user.save(update_fields=["is_active"])  
            return user  
            
    def validate(self, value):
        user = PmsUser(**value)
        password = value.get("password")
        
        if PmsUser.objects.filter(email=value.get("email")).exists():
            raise serializers.ValidationError({"email":"EmailAlready exists"}) 
        
        try:
            validate_password(password, user)
            
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError({"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}) 
        
        return value         
   
   
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                    required=True, 
                                    validators=[validate_password])   
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = PmsUser
        fields=[
            "old_password",
            "password",
            "password2",
        ]
        
    def validate(self, value):
        if value["password"] !=value["password2"]:
            raise serializers.ValidationError({"password":"pasword field donot match"})
        return value
    
    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old password":"old password donot match"})
        
    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save() 
        return instance
    
               
               
class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if PmsUser.objects.filter(email=email).exists():
            user = PmsUser.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link', link)
            # Send EMail
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):   
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = PmsUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')
        
        
class PmsUserProfileSerializer(serializers.ModelSerializer):
    user = PmsUser
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    
    class Meta:
        model = PmsUserDetails  
        fields = tuple(["first_name", "last_name", "user"])
              