#from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import *
from django.contrib.auth import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
#from django.shortcuts import render_to_response
from django.template import RequestContext
from django_filters.rest_framework import DjangoFilterBackend


from django.shortcuts import *

# Import models
from django.db import models
from django.contrib.auth.models import *
from api.models import *

#REST API
from rest_framework import viewsets, filters, parsers, renderers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import *
from rest_framework.decorators import *
from rest_framework.authentication import *

#filters
#from filters.mixins import *

from api.pagination import *
import json, datetime, pytz
from django.core import serializers
import requests


def home(request):
   """
   Send requests to / to the ember.js clientside app
   """
   return render_to_response('ember/index.html',
               {}, RequestContext(request))

def xss_example(request):
  """
  Send requests to xss-example/ to the insecure client app
  """
  return render_to_response('dumb-test-app/index.html',
              {}, RequestContext(request))

class Register(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Login
        username = request.POST.get('username') #you need to apply validators to these
        print username
        password = request.POST.get('password') #you need to apply validators to these
        email = request.POST.get('email') #you need to apply validators to these
        gender = request.POST.get('gender') #you need to apply validators to these
        age = request.POST.get('age') #you need to apply validators to these
        educationlevel = request.POST.get('educationlevel') #you need to apply validators to these
        city = request.POST.get('city') #you need to apply validators to these
        state = request.POST.get('state') #you need to apply validators to these

        print request.POST.get('username')
        if User.objects.filter(username=username).exists():
            return Response({'username': 'Username is taken.', 'status': 'error'})
        elif User.objects.filter(email=email).exists():
            return Response({'email': 'Email is taken.', 'status': 'error'})

        #especially before you pass them in here
        newuser = User.objects.create_user(email=email, username=username, password=password)
        newprofile = Profile(user=newuser, gender=gender, age=age, educationlevel=educationlevel, city=city, state=state)
        newprofile.save()

        return Response({'status': 'success', 'userid': newuser.id, 'profile': newprofile.id})

class Session(APIView):
    permission_classes = (AllowAny,)
    def form_response(self, isauthenticated, userid, username, error=""):
        data = {
            'isauthenticated': isauthenticated,
            'userid': userid,
            'username': username
        }
        if error:
            data['message'] = error

        return Response(data)

    def get(self, request, *args, **kwargs):
        # Get the current user
        if request.user.is_authenticated():
            return self.form_response(True, request.user.id, request.user.username)
        return self.form_response(False, None, None)

    def post(self, request, *args, **kwargs):
        # Login
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return self.form_response(True, user.id, user.username)
            return self.form_response(False, None, None, "Account is suspended")
        return self.form_response(False, None, None, "Invalid username or password")

    def delete(self, request, *args, **kwargs):
        # Logout
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class Events(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (parsers.JSONParser,parsers.FormParser)
    renderer_classes = (renderers.JSONRenderer, )


class ActivateIFTTT(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (parsers.JSONParser,parsers.FormParser)
    renderer_classes = (renderers.JSONRenderer, )

class DogList(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (parsers.JSONParser,parsers.FormParser)
    renderer_classes = (renderers.JSONRenderer, )

    def get(self, request, format=None):
        dogs = Dog.objects.all()
        json_data = serializers.serialize('json', dogs)
        content = {'dogs': json_data}
        return HttpResponse(json_data, content_type='json')

    def post(self, request):
        print 'REQUEST DATA'
        print str(request.data)

        name = request.data.get('name')
        age = int(request.data.get('age'))
        breed = request.data.get('breed')
        gender = request.data.get('gender')
        color = request.data.get('color')
        favoritefood = request.data.get('favoritefood')
        favortietoy = request.data.get('favortietoy')

        print 'test1'
        newDog = Dog(
            name=name,
            age=age,
            breed=breed,
            gender=gender,
            color=color,
            favoritefood=favoritefood,
            favortietoy=favortietoy
        )

        print 'test2'
        try:
            newDog.clean_fields()
        except ValidationError as e:
            print e
            return Response({'success':False, 'error':e}, status=status.HTTP_400_BAD_REQUEST)

        newDog.save()
        print 'New Dog named: ' + name
        return Response({'success': True}, status=status.HTTP_200_OK)

class DogDetail(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (parsers.JSONParser,parsers.FormParser)
    renderer_classes = (renderers.JSONRenderer, )

    def get_object(self, pk):
        try:
            return Dog.objects.get(pk=pk)
        except Dog.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dog = self.get_object(pk)
        json_data = serializers.serialize('json', dog)
        content = {'dog': json_data}
        return HttpResponse(json_data, content_type='json')
    
    def put(self, request, pk, format=None):
        dog = self.get_object(pk)

        dog.name = request.data.get('name')
        dog.age = int(request.data.get('age'))
        dog.breed = request.data.get('breed')
        dog.gender = request.data.get('gender')
        dog.color = request.data.get('color')
        dog.favoritefood = request.data.get('favoritefood')
        dog.favortietoy = request.data.get('favortietoy')

        try:
            dog.clean_fields()
        except ValidationError as e:
            print e
            return Response({'success':False, 'error':e}, status=status.HTTP_400_BAD_REQUEST)

        dog.save()
        return Response({'success': True}, status=status.HTTP_200_OK)


    def delete(self, request, pk, format=None):
        dog = self.get_object(pk)
        dog.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)

class BreedList(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (parsers.JSONParser,parsers.FormParser)
    renderer_classes = (renderers.JSONRenderer, )

    def get(self, request, format=None):
        breeds = Breed.objects.all()
        json_data = serializers.serialize('json', breed)
        content = {'dogs': json_data}
        return HttpResponse(json_data, content_type='json')

    def post(self, request):
        print 'REQUEST DATA'
        print str(request.data)

        name = request.data.get('name')
        size = request.data.get('size')
        friendliness = int(request.data.get('friendliness'))
        trainability = int(request.data.get('trainability'))
        sheddingamount = int(request.data.get('sheddingamount'))
        exerciseneeds = int(request.data.get('exerciseneeds'))

        print 'test1'
        newBreed = Breed(
            name=name,
            size = size[0],
            friendliness = friendliness,
            trainability = trainability,
            sheddingamount = sheddingamount,
            exerciseneeds = exerciseneeds
        )

        print 'test2'
        try:
            newDog.clean_fields()
            if not 1 <= newBreed.friendliness <= 5 or not 1 <= trainability <= 5 or not 1 <= sheddingamount <= 5 or not 1 <= exerciseneeds <= 5:
                return Response({'success':False, 'error':e}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            print e
            return Response({'success':False, 'error':e}, status=status.HTTP_400_BAD_REQUEST)

        newDog.save()
        print 'New Dog named: ' + name
        return Response({'success': True}, status=status.HTTP_200_OK)

class BreedDetail(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (parsers.JSONParser,parsers.FormParser)
    renderer_classes = (renderers.JSONRenderer, )

    def get_object(self, pk):
        try:
            return Breed.objects.get(pk=pk)
        except Breed.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        breed = self.get_object(pk)
        json_data = serializers.serialize('json', breed)
        content = {'breed': json_data}
        return HttpResponse(json_data, content_type='json')
    
    def put(self, request, pk, format=None):
        breed = self.get_object(pk)

        breed.name = request.data.get('name')
        breed.age = int(request.data.get('age'))
        breed.breed = request.data.get('breed')
        breed.gender = request.data.get('gender')
        breed.color = request.data.get('color')
        breed.favoritefood = request.data.get('favoritefood')
        breed.favortietoy = request.data.get('favortietoy')

        try:
            breed.clean_fields()
            if not 1 <= newBreed.friendliness <= 5 or not 1 <= trainability <= 5 or not 1 <= sheddingamount <= 5 or not 1 <= exerciseneeds <= 5:
                return Response({'success':False, 'error':e}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            print e
            return Response({'success':False, 'error':e}, status=status.HTTP_400_BAD_REQUEST)

        breed.save()
        return Response({'success': True}, status=status.HTTP_200_OK)


    def delete(self, request, pk, format=None):
        breed = self.get_object(pk)
        breed.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)