from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer, TokenSerializer
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import uuid
import hashlib
from .models import Token

#jallnuniqpqmyxca

# Create your views here.
class TestView(APIView):
    def get(self, request, format=None):
        print("API was called")
        return Response("You Made It", status=200)


class UserView(APIView):
    def post(self, request, format=None):
        print("creating a user")
        user_data = request.data
        user_data['is_active'] = False

        user_serializer= UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=False):
            user_serializer.save()

            salt = uuid.uuid4().hex
            hash_object = hashlib.sha256(salt.encode()+ str(user_serializer.data['id']).encode())
            token = hash_object.hexdigest()+':'+salt

            token_serializer = TokenSerializer(data={"user":user_serializer.data['id'], "token":token})
            if token_serializer.is_valid(raise_exception=True):
                token_serializer.save()


            message = Mail(
                from_email="gameplay.anything85@gmail.com",
                to_emails=user_data['email'],
                subject='Por favor confirme su dirección de correo electrónico',
                html_content=f"\
                    Hola {user_data['first_name']},\<br><br>\Gracias por registrarte. Para confirmar su dirección de correo electrónico, haga clic <a href='http://localhost:8000/api/v1/user/verify-user/{token}'>aqui</a>",
            )

            try:
                sg = SendGridAPIClient("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")
                response = sg.send(message)
                return Response(user_serializer.data, status=200)
            except Exception as e:
                print("ERROR", e)
        else:
            print(user_serializer.errors)
        
        return Response({"Msg": "ERR"}, status=400)
    

class UserVerificationView(APIView):
    def get(self, request, pk, format=None):
        print("VERIFYING USER", pk)

        tokenObj= Token.objects.filter(token=pk).first()
        user = User.objects.filter(id=tokenObj.user.id).first()
        
        if user:
            user_serializer = UserSerializer(user, data={'is_active': True}, partial=True)
            if user_serializer.is_valid(raise_exception=False):
                user_serializer.save()

                return Response("successful verification",status=200)
            
        return Response("Without Verification",status=404)


class UserLoginView(APIView):
    #Convert a user token into user data
    def get(self, request, format=None):
        if request.user.is_authenticated == False or request.user.is_active == False:
            return Response("Invalid Credentials", status=403)

        user = UserSerializer(request.user)

        return Response(user.data, status=200)
    
    def post(self, request, format=None):
        print("Login Class")

        user_obj = User.objects.filter(email = request.data['username']).first() or User.objects.filter(username=request.data['username']).first()
        
        if user_obj is not None:
            credentials = {
                'username': user_obj.username,
                'password': request.data['password']
            }
            user = authenticate(**credentials)

            if user and user.is_active:
                user_serializer = UserSerializer(user)
                return Response(user_serializer.data, status=200)

        return Response("Invalid Credentials", status=403)

