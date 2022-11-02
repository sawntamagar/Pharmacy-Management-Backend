from datetime import datetime
from django.shortcuts import  get_object_or_404


from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated


from account.models import PmsUser, PmsUserDetails
from account.serializers import(
    PmsUserCreateSerializer, PmsTokenObtainPairSerializer,
    ChangePasswordSerializer, ForgetPasswordSerializer,
    PmsUserProfileSerializer,ResetPasswordSerializer
)
from common_utils.emails import send_email
from account import signals
# from common_utils.reset_email_pass import send_reset_email
from account.constants import (
    _SUCCESS_REGISTER_MESSAGE, _EMAIL_VERIFIED,
    _PASSWORD_RESET_EMAIL_SENT, _INVALID_TOKEN_LINK,
    _PASSWORD_CHANGED, _SUCCESS_PROFILE_SETUP,
)

class PmsTokenObtainPairView(TokenObtainPairView):
    serializer_class = PmsTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


class PmsUserRegisterViewSet(viewsets.ModelViewSet):
    queryset = PmsUser.objects.all()
    serializer_class = PmsUserCreateSerializer
    
    def get_serializer_class(self):
        return super().get_serializer_class()
        
    def get_queryset(self):
        return super().get_queryset()
    
    def retrieve(self, request, pk=None): 
        queryset = PmsUser.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()
        signals.user_registered.send(sender=PmsUserRegisterViewSet, user=user,
                                     request=self.request) 
        context={"user":user}
        send_email(user.email, self.request, context, user)   
        return user
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # self.perform_create(serializer)
        #creating user id so need to replace self.perform.create with 
        #variable as user
        user = self.perform_create(serializer)
        
        #adding profile to Pmsuser
        user_details = {
            "user":user.id,
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"), 
        }   
        userProfileSerializer = PmsUserProfileSerializer(data=user_details)
        userProfileSerializer.is_valid(raise_exception=True)
        profile = userProfileSerializer.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response({'message': _SUCCESS_REGISTER_MESSAGE},
                        status = status.HTTP_201_CREATED,
                        headers = headers)    
        
    @action(detail=False, methods=["get"], url_path="profile")
    def profile(self, request, *args, **kwargs):  #TODO setup serializer
        user_profile = PmsUserDetails.objects.get(user=request.user)
        return Response(PmsUserProfileSerializer(user_profile).data, status=status.HTTP_200_OK)
        
    
    @action(detail=False, methods=["patch"], url_path="update-profile")
    def update_profile(self, request, *args, **kwargs): #TODO setup serializer
        user_profile = PmsUserDetails.objects.filter(user=request.user)
        user_profile.update(**request.data)
        
        return Response(
            PmsUserProfileSerializer(PmsUserDetails.objects.get(user=request.user).data,
                                     status=status.HTTP_200_OK)
        ) 
    
        
    @action(detail=False, methods=["post"], url_path="activate-account")
    def activate_account(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        user=serializer.user
        user.is_active=True
        user.email_confirmed_on = datetime.utcnow()
        user.save()
        return Response({"messgae":_EMAIL_VERIFIED},
                        status=status.HTTP_200_OK)
        
    def update(self, request, *args, **kwargs):
        return Response({"message": _EMAIL_VERIFIED},
                        status=status.HTTP_200_OK)    


class ChangePasswordView(generics.UpdateAPIView):
    queryset = PmsUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    
# class ForgetPasswordView(generics.CreateAPIView):
#     queryset = PmsUser.objects.all()
#     # permission_classes = (IsAuthenticated,)
#     serializer_classes = ForgetPasswordSerializer
    
#     def get_serializer_class(self):
#         return super().get_serializer_class()
        
    
#     def create(self,*args, **kwargs):
#         serializer =self.get_serializer
#         serializer.is_valid(raise_exception=True)
#         return Response({"messgae": _PASSWORD_RESET_EMAIL_SENT},
#                         status=status.HTTP_200_OK)
#     # def create(self,*args, **kwargs):
#     #     user = self.request.user
#     #     token = PmsUser.objects.get_token(user.email)
#     #     print(token)
#     #     send_reset_email(user, token)
#     #     return Response({"messgae": _PASSWORD_RESET_EMAIL_SENT},
#     #                     status=status.HTTP_200_OK)
    
# class ResetPasswordView(generics.UpdateAPIView):
#     queryset = PmsUser.objects.all()
#     # permission_classes = (IsAuthenticated,)
#     def get_queryset(self):
#         return self.queryset.filter(id=self.request.user.id)
    
#     def patch(self, request, uid,token,*args, **kwargs):
#         serializer = ResetPasswordSerializer(data=request.data, context={'uid':uid, 'token':token})
#         serializer.is_valid(raise_exception=True)
#         return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
          
        
class ForgetPasswordView(APIView):
    # renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': _PASSWORD_RESET_EMAIL_SENT},
                        status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    def post(self, request, uid, token, format=None):
        serializer = ResetPasswordSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':_PASSWORD_CHANGED}, status=status.HTTP_200_OK)
    
    
class PmsUserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = PmsUserProfileSerializer 
    queryset = PmsUserDetails.objects.all()
    permission_classes=[IsAuthenticated]
    
    def create(self,request, *args, **kwargs):
        profile_data = request.data
        profile_data["user"] = request.user.id
        serializer = self.get_serializer(data=profile_data)
        serializer.is_valid(raise_exception= True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response({"message": _SUCCESS_PROFILE_SETUP},
                        status=status.HTTP_201_CREATED, headers=headers)
        
    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)   
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)
        
        