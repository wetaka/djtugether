from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from tugether.models import User, Event, Comment, Category
from tugether.serializers import UserSerializer, EventSerializer, CommentSerializer, CategorySerializer
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser


# Create your views here.

@csrf_exempt
def user_list(request):
    """
    List all code user, or create a new user.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        print('1. test: post request')
        print(request)
        data = JSONParser().parse(request)
        print('2. test: post request')
        print(data)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        print("Error jaaaa :")
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def user_detail(request, pk):
    """
    Retrieve, update or delete a code .
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

        user.delete()
        return HttpResponse(status=204)

# @csrf_exempt
# @parser_classes((JSONParser,))
# def login(request):
#     if request.method == 'POST':   
#         try:
#             data = JSONParser().parse(request)
#             User.objects.get(userid=data['userid'], firstname=data['firstname'])
#             token = data['userid'] + 'xxxxx' + data['firstname'] + 'yyyyy'
#             return JsonResponse({'token': token}, status=201)
#         except User.DoesNotExist:
#             return HttpResponse(status=401)


@csrf_exempt
@parser_classes((JSONParser,))
def check_login(request, userid):
    if request.method == 'GET':
        try:
            user = User.objects.get(userid=userid)
            return HttpResponse(status=200)
        except User.DoesNotExist:
            return HttpResponse(status=404)


    
@csrf_exempt
def event_list(request):
    """
    List all code event, or create a new event.
    """
    if request.method == 'GET':
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def event_detail(request, pk):
    """
    Retrieve, update or delete a code .
    """
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EventSerializer(event, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        event.delete()
        return HttpResponse(status=204)



@csrf_exempt
def comment_list(request):
    """
    List all code user, or create a new user.
    """
    if request.method == 'GET':
        comment = Comment.objects.all()
        serializer = CommentSerializer(comment, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def comment_detail(request, pk):
    """
    Retrieve, update or delete a code .
    """
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CommentSerializer(comment, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        comment.delete()
        return HttpResponse(status=204)

@csrf_exempt
def category_list(request):
    """
    List all code category, or create a new category.
    """
    if request.method == 'GET':
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def category_detail(request, pk):
    """
    Retrieve, update or delete a code .
    """
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        print("Error jaaaa :")
        print(data)
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        category.delete()
        return HttpResponse(status=204)
