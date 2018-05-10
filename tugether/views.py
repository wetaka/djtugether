from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from tugether.models import User, Event, Comment, Category, Noti
from tugether.serializers import UserSerializer, EventSerializer, CommentSerializer, CategorySerializer ,NotiSerializer
from rest_framework.decorators import parser_classes, api_view
from rest_framework.parsers import JSONParser

from datetime import datetime, date
import time
# import datatime

from django.db.models import Q


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
@parser_classes((JSONParser,))
def get_yourevent(request, userid):
    if request.method == 'GET':
        try:
            event = Event.objects.all().filter(createby=userid)
            serializer = EventSerializer(event, many=True)                     

            result = serializer.data    
            max_size = len(result)
            
            query_string = request.GET
            if 'st' in query_string  and 'ed' in query_string:
                st = int(query_string['st'])
                ed = int(query_string['ed'])
                result = result[st : ed]
            elif 'st' in query_string:
                st = int(query_string['st'])
                result = result[st:]
            elif 'ed' in query_string:
                ed = int(query_string['ed'])                
                result = result[:ed]
            
            return JsonResponse({ "max_size": max_size, "data": result }, safe=False)
            
        except Event.DoesNotExist:
            return HttpResponse(status=404)

@csrf_exempt
@parser_classes((JSONParser,))
def get_join(request, eventid):
    if request.method == 'GET':
        try:
            event = Event.objects.get(id=eventid)
            serializer = EventSerializer(event)
            print(serializer.data['join'])
            
            user = User.objects.all().filter(userid__in=list(serializer.data['join']))

            print(user)

            user_serializer = UserSerializer(user, many=True)
                     
        except Event.DoesNotExist:
            return HttpResponse(status=404)


@csrf_exempt
@parser_classes((JSONParser,))
@api_view(['GET'])
def get_searchevent(request, categoryid):
    print("DateTime jaaaaaaaaa ")
    if request.method == 'GET':
        try:
            query_string = request.GET

            date_now = datetime(2010,1,26,0,0,0)
            date_modified = datetime.now()
            print(date_modified)
            print("DateTime jaaaaaaaaa ")
            print(date_modified)
            print("DateTime jaaaaaaaaa ")
            print(datetime(2000,1,1,0,0,0))
            print("DateTime jaaaaaaaaa ")
            
            if 'searchword' in query_string :
                searchword = query_string['searchword']
                category = Category.objects.all().filter(categoryname__icontains=searchword ).values_list('pk', flat=True)
                print(category)

                if categoryid == 0 :
                    event = Event.objects.all().filter(Q(topic__icontains=searchword) | Q(hashtag__icontains=searchword) | Q(description__icontains=searchword) | Q(categoryid__in=list(category)) ,eventenddate__gt=date_now).distinct()
                else :   
                    event = Event.objects.all().filter(Q(topic__icontains=searchword) | Q(hashtag__icontains=searchword) | Q(description__icontains=searchword) | Q(categoryid__in=list(category)) ,eventenddate__gt=date_now , categoryid = categoryid).distinct()
            
                print(event)

                serializer = EventSerializer(event, many=True)
                category_serializer = list(category)
                print(serializer.data)
                print(category_serializer)
                # print(category)
                for et in serializer.data :
                    et['total'] = 0

                    if et['topic'].find(searchword) != -1 :
                        et['total'] = et['total'] + 100

                    etsplit = et['hashtag'].split('#')
                    for  sp in etsplit :
                        if sp.find(searchword) != -1 :
                            et['total'] = et['total'] + 30

                    if et['description'].find(searchword) != -1 :
                        et['total'] = et['total'] + 40
                                    
                    datetable = datetime(*time.strptime(et['eventenddate'][:19], "%Y-%m-%dT%H:%M:%S")[:6])
                    diff = datetable - date_now
                    # # b = ((diff.total_seconds() /60) / 60)/24
                    print(diff)
                    # a = diff.days * (-5)
                    et['total'] = et['total'] + (diff.days * (-5))

                    for ct in category_serializer :
                        print(et['categoryid'])
                        for ec in et['categoryid'] :
                            if ct == ec :
                                et['total'] = et['total'] + 25    
                                
                result = sorted(serializer.data, key=lambda data : data['total'], reverse=True)     
                max_size = len(result)
                print('--------------------------------------------')
                print(max_size)
            
            else :
                if categoryid == 0 :
                    event = Event.objects.all().filter(eventenddate__gt=date_now).distinct()
                else :   
                    event = Event.objects.all().filter(eventenddate__gt=date_now, categoryid = categoryid).distinct()

                serializer = EventSerializer(event, many=True)
                
                print(serializer.data)
                
                for et in serializer.data :
                    et['total'] = 0
                                    
                    datetable = datetime(*time.strptime(et['eventenddate'][:19], "%Y-%m-%dT%H:%M:%S")[:6])
                    diff = datetable - date_now
                    print(diff)
                    et['total'] = et['total'] + (diff.days * (-5))  
                                
                result = sorted(serializer.data, key=lambda data : data['total'], reverse=True)     
                max_size = len(result)
                print('--------------------------------------------')
                print(max_size)
                       

            if 'st' in query_string  and 'ed' in query_string:
                st = int(query_string['st'])
                ed = int(query_string['ed'])
                result = result[st : ed]
            elif 'st' in query_string:
                st = int(query_string['st'])
                result = result[st:]
            elif 'ed' in query_string:
                ed = int(query_string['ed'])                
                result = result[:ed]
            
            return JsonResponse({ "max_size": max_size, "data": result }, safe=False)
        except Event.DoesNotExist:
            return HttpResponse(status=404)

@csrf_exempt
@parser_classes((JSONParser,))
@api_view(['GET'])
def get_autoCompleteWords(request,word ,categoryid):
    print("DateTime jaaaaaaaaa ")
    if request.method == 'GET':
        try:
            # query_string = request.GET          
            date_now = datetime(2010,1,26,0,0,0)
            date_modified = datetime.now()
            print(date_modified)
            print("DateTime jaaaaaaaaa ")
            print(date_modified)
            print("DateTime jaaaaaaaaa ")
            print(datetime(2000,1,1,0,0,0))
            print("DateTime jaaaaaaaaa ")
            print("DateTime jaaaaaaaaa ")
            print("DateTime jaaaaaaaaa ")
            
            # if 'searchword' in query_string :
                # searchword = query_string['searchword']
            category = Category.objects.all().filter(categoryname__icontains=word ).values_list('pk', flat=True)
            print(category)

            if categoryid == 0 :
                event = Event.objects.all().filter(Q(topic__icontains=word) | Q(hashtag__icontains=word) | Q(description__icontains=word) | Q(categoryid__in=list(category)) ,eventenddate__gt=date_now).distinct()
            else :   
                event = Event.objects.all().filter(Q(topic__icontains=word) | Q(hashtag__icontains=word) | Q(description__icontains=word) | Q(categoryid__in=list(category)) ,eventenddate__gt=date_now , categoryid = categoryid).distinct()
        
            print(event)

            serializer = EventSerializer(event, many=True)
            category_serializer = list(category)
            print(serializer.data)
            print(category_serializer)
            # print(category)

            allwords = {}

            for et in serializer.data :
                # et['total'] = 0
                allstr = et['topic']+" "+et['description']+" "+et['hashtag']
                splitwords = allstr.split(" ")

                print("+++++++++++++++++++++++++++++++++++++++++++++")
                print(splitwords)

                for inwords in splitwords :
                    print(inwords)
                    if inwords.find(word) != -1 :
                        # print(allwords[inwords])
                        if inwords in allwords :
                            allwords[inwords] = allwords[inwords] + 1
                            print("55555555555555555555555555")
                            print(allwords[inwords])

                        else :
                            allwords[inwords] = 1 

            # print("*************************++++++++++++++++++++++++++++++++++++")
            # print(allwords)

            sorted_allwords = sorted(allwords, key=allwords.get, reverse=True)
            # sorted_allwords = [(k, allwords[k]) for k in sorted(allwords, key=allwords.values, reverse=True)]
            # dict.values(sorted)
            # print("-------------------------------------------")
            # print(sorted_allwords)
            # print("/////////////////////////////////////////////////////////////////")
            # print(sorted_allwords.keys())
            result = sorted_allwords[0 : 9]
            # print("**************************************************")
            # print(allwords.values())
            # print("----------------------------------------//////////////////////////////////")
            # print(result) 
            return JsonResponse({"data": result }, safe=False)
        except Event.DoesNotExist: 
            return HttpResponse(status=404)

@csrf_exempt
@parser_classes((JSONParser,))
def get_upcomingevent(request, userid):
    print("DateTime jaaaaaaaaa ")
    if request.method == 'GET':
        try:
            date_now = datetime(2000,10,26,0,0,0)
            date_modified = datetime.now()
            print(date_modified)
            print("DateTime jaaaaaaaaa ")
            print(date_modified)
            print("DateTime jaaaaaaaaa ")
            print(datetime(2000,1,1,0,0,0))
            print("DateTime jaaaaaaaaa ")

            event = Event.objects.all().filter(join__in=[userid] ,eventenddate__gt=date_now).distinct()

            print(event)
           
            serializer = EventSerializer(event, many=True)
           
            print(serializer.data)
           
            for et in serializer.data :
                et['total'] = 0
                                
                datetable = datetime(*time.strptime(et['eventstdate'][:19], "%Y-%m-%dT%H:%M:%S")[:6])
                diff = datetable - date_now
                # # b = ((diff.total_seconds() /60) / 60)/24

                print("Upcoming dayssssssss")
                print(diff)
                # a = diff.days * (-5)
                et['total'] = et['total'] + (diff.days * (-5))
             
            
            print(serializer.data)
            result = sorted(serializer.data, key=lambda data : data['total'], reverse=True)
            max_size = len(result)
            print('--------------------------------------------')
            print(max_size)
        
        # else :
            query_string = request.GET

            if 'st' in query_string  and 'ed' in query_string:
                st = int(query_string['st'])
                ed = int(query_string['ed'])
                result = result[st : ed]
            elif 'st' in query_string:
                st = int(query_string['st'])
                result = result[st:]
            elif 'ed' in query_string:
                ed = int(query_string['ed'])                
                result = result[:ed]
            
            return JsonResponse({ "max_size": max_size, "data": result }, safe=False)
            
        except Event.DoesNotExist:
            return HttpResponse(status=404)

@csrf_exempt
@parser_classes((JSONParser,))
def get_pastevent(request, userid):
    print("DateTime jaaaaaaaaa ")
    if request.method == 'GET':
        try:
            date_now = datetime(2020,10,26,0,0,0)
            date_modified = datetime.now()
            print(date_modified)
            print("DateTime jaaaaaaaaa ")
            print(date_modified)
            print("DateTime jaaaaaaaaa ")
            print(datetime(2000,1,1,0,0,0))
            print("DateTime jaaaaaaaaa ")
        
            event = Event.objects.all().filter(eventenddate__lt=date_now, join__in=[userid]).distinct()

            print(event)

  
            serializer = EventSerializer(event, many=True)

        
            print(serializer.data)
        
            for et in serializer.data :
                et['total'] = 0
                                
                datetable = datetime(*time.strptime(et['eventenddate'][:19], "%Y-%m-%dT%H:%M:%S")[:6])
                diff = datetable - date_now
                # # b = ((diff.total_seconds() /60) / 60)/24
                print(diff)
                # a = diff.days * (-5)
                et['total'] = et['total'] + (diff.days * (-5))

            print(serializer.data)
            result = sorted(serializer.data, key=lambda data : data['total'], reverse=True)
            max_size = len(result)
            print('--------------------------------------------')
            print(max_size)
        

            query_string = request.GET
                      
            if 'st' in query_string  and 'ed' in query_string:
                st = int(query_string['st'])
                ed = int(query_string['ed'])
                result = result[st : ed]
            elif 'st' in query_string:
                st = int(query_string['st'])
                result = result[st:]
            elif 'ed' in query_string:
                ed = int(query_string['ed'])                
                result = result[:ed]
            
            return JsonResponse({ "max_size": max_size, "data": result }, safe=False)

            # return JsonResponse(result , safe=False)
            
        except Event.DoesNotExist:
            return HttpResponse(status=404)



@csrf_exempt
@parser_classes((JSONParser,))
def get_comment(request, eventid):
    if request.method == 'GET':
        try:
            # event = Event.objects.get(id=eventid)
            # serializer = EventSerializer(event)
            # print(serializer.data['join'])
            # event = Event.objects.all().filter(Q(topic__icontains=searchword) | Q(hashtag__icontains=searchword) | Q(description__icontains=searchword) | Q(categoryid__in=list(category)) ,eventenddate__gt=date_now).distinct()
            
            comment = Comment.objects.order_by('createdate').filter(eventid = eventid)
            print(comment)
            # print(user)
            # Comment.objects.order_by('createdate')

            comment_serializer = CommentSerializer(comment, many=True)
            # print(comment_serializer.data)
            return JsonResponse(comment_serializer.data , safe=False)     

        except Event.DoesNotExist:
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
        date_modified = datetime.now()
        data['createdate'] = date_modified
        data['bcapprove'] = ""
        data['posterpic'] = ""
        data['updatedate'] = None
        data['active'] = true
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


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
        print("=================")
        date_modified = datetime.now()
        print(data)
        print(data['createby'])
        data['createdate'] = date_modified
        print(data)
        serializer = CommentSerializer(data=data)
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


# add Noti
@csrf_exempt
def noti_list(request):
    """
    List all code event, or create a new event.
    """
    if request.method == 'GET':
        noti = Noti.objects.all()
        serializer = NotiSerializer(noti, many=True)  
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NotiSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def noti_detail(request, pk):
    """
    Retrieve, update or delete a code .
    """
    try:
        noti = Noti.objects.get(pk=pk)
    except Noti.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = NotiSerializer(noti)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = NotiSerializer(noti, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        noti.delete()
        return HttpResponse(status=204)

# ---------------------------------------------------------------------------
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
