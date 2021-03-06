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
import requests
from django.db.models import Q
from django.contrib.auth import get_user_model
# User = get_user_model()
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
        print(type(data))
        # print(data)
        serializer = UserSerializer(data=data)
        print("***********************************")
        print(serializer)
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
    # print('---------------------------------')
    # print(request.user.username)
    # print('dawdawdwadwadwa awdaw awdaw dawd ')
    # if request.method == 'GET':
    #     user = request.user
    #     print(user)
    #     print(type(user))
    #     serializer = UserSerializer(user)
    #     return JsonResponse(serializer.data, status=200)
        
        try:
            user = User.objects.get(userid=userid)
            # user = request.user
            serializer = UserSerializer(user)
            return HttpResponse(serializer.data)
        except User.DoesNotExist:
            return HttpResponse(status=404)


@csrf_exempt
@parser_classes((JSONParser,))
def get_yourevent(request, userid):
    if request.method == 'GET':
        try:
            event = Event.objects.all().filter(createby=userid, approve="2")
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
def get_youreventwait(request, userid):
    if request.method == 'GET':
        try:
            event = Event.objects.all().filter(createby=userid,approve="1")
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

            return JsonResponse(user_serializer.data, safe=False)            
                     
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
            print("Input")
            print(query_string)
            # date_now = datetime(2010,1,26,0,0,0)
            date_now = datetime.now()
            date_modified = datetime.now()
            print(date_modified)
            print("DateTime jaaaaaaaaa ")
            print(date_modified)
            print("DateTime jaaaaaaaaa ")
            print(datetime(2000,1,1,0,0,0))
            print("DateTime jaaaaaaaaa ")

            # print()
            
            if 'searchword' in query_string :
                searchword = query_string['searchword']
                category = Category.objects.all().values_list('pk', flat=True)
                print(category)

                if categoryid == 0 :
                    print('cate =============.====================================')
                    event = Event.objects.all().filter(Q(topic__icontains=searchword) | Q(hashtag__icontains=searchword), approve="2").distinct()
                else :   
                    event = Event.objects.all().filter(Q(topic__icontains=searchword) | Q(hashtag__icontains=searchword), categoryid = categoryid, approve="2").distinct()
            
                print(event)

                serializer = EventSerializer(event, many=True)
                category_serializer = list(category)
                print('result ============================================')
                print(serializer.data)
                print(category_serializer)
                # print(category)
                for et in serializer.data :
                    et['total'] = 0
                    if et['topic'] is None :
                        et['topic'] = ''
                    if et['description'] is None:
                        et['description'] = ''
                    if et['hashtag'] is None:
                        et['hashtag'] = ''

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
                    print(diff)
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
                    event = Event.objects.all().filter(eventenddate__gt=date_now,approve="2").distinct()
                else :   
                    event = Event.objects.all().filter(eventenddate__gt=date_now, categoryid = categoryid, approve="2").distinct()

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

            print("Output")
            print(result)
            
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
            # datetime.now()        
            # date_now = datetime(2010,1,26,0,0,0)
            date_now = datetime.now()
            
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
                event = Event.objects.all().filter(Q(topic__icontains=word) | Q(hashtag__icontains=word) | Q(description__icontains=word) | Q(categoryid__in=list(category)) ,approve="2").distinct()
            else :   
                event = Event.objects.all().filter(Q(topic__icontains=word) | Q(hashtag__icontains=word) | Q(description__icontains=word) | Q(categoryid__in=list(category)) , categoryid = categoryid,approve="2").distinct()
        
            print(event)

            serializer = EventSerializer(event, many=True)
            category_serializer = list(category)
            print(serializer.data)
            print(category_serializer)
            # print(category)

            allwords = {}

            for et in serializer.data :
                # et['total'] = 0
                if et['topic'] is None :
                    et['topic'] = ''
                if et['description'] is None:
                    et['description'] = ''
                if et['hashtag'] is None:
                    et['hashtag'] = ''
                
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
            # date_now = datetime(2000,10,26,0,0,0)
            date_now = datetime.now()
            
            # date_modified = datetime.now()
            # datetime.now()
            # print(date_modified)
            # print("DateTime jaaaaaaaaa ")
            # print(date_modified)
            print("DateTime jaaaaaaaaa ")
            print(datetime(2000,1,1,0,0,0))
            # print("DateTime jaaaaaaaaa ")

            event = Event.objects.all().filter(join__in=[userid] ,eventenddate__gt=date_now, approve="2").distinct()

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
            print(serializer.errors)
            return HttpResponse(status=404)

@csrf_exempt
@parser_classes((JSONParser,))
def get_pastevent(request, userid):
    print("DateTime jaaaaaaaaa ")
    if request.method == 'GET':
        try:
            # date_now = datetime(2020,10,26,0,0,0)
            date_now = datetime.now()
            date_modified = datetime.now()
            print(date_modified)
            print("DateTime jaaaaaaaaa ")
            print(date_modified)
            print("DateTime jaaaaaaaaa ")
            print(datetime(2000,1,1,0,0,0))
            print("DateTime jaaaaaaaaa ")
        
            event = Event.objects.all().filter(eventenddate__lt=date_now, join__in=[userid],approve="2").distinct()

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
        event = Event.objects.all().filter(approve="2")
        serializer = EventSerializer(event, many=True)  
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        date_modified = datetime.now()
        data['createdate'] = date_modified
        data['bcapprove'] = ""
        # data['posterpic'] = "555"
        data['updatedate'] = None
        data['active'] = True
        data['approve'] = "1"
        print(data)
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print("serializer.data : =======================")
            print(serializer.data)
            return JsonResponse(serializer.data, status=201)
        print(serializer.errors)
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
        print("=================")
        date_modified = datetime.now()
        print(data)
        # print(data['createby'])
        data['updatedate'] = date_modified
        print(data)

        serializer = EventSerializer(event, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        print(serializer.errors)
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


# @csrf_exempt
# @parser_classes((JSONParser,))
# def redirectURL(request) :
#     print('================== redirectURL ==================')
#     query_string = request.GET
#     code = query_string['code']
#     print(query_string)
#     print(' code   '+code)
#     # client_res = request.get('https://www.google.com/')
#     data = {
#         'code' : code,
#         'client_id' : 'Qzw4Fnulqrb1Mswk9nYUEUi2rHOHeyKClwq2IM1X',
#         'client_secret' : 'OSwcfymQOUAG4AqIqe0ZlOR8PUR0V7KgXLaxpT9PLGLLoNO52CrBVEJMDd6g0ACtfLxOLnqFIuHxrH5Ie1L3cRE3TGCXlw35mNhEWXLSMiP94qd6d8X9VZECTi5uAgvO' ,
#         'redirect_uri' : 'http://172.25.79.42:8000/api/redirect/tu/' ,
#         'grant_type' : 'authorization_code'
#     }

#     client_res = requests.post('https://api.tu.ac.th/o/token/' , data = data)
#     print('============client_res==============')
#     print(client_res.json())
#     # print(client_res.json()['access_token'])
#     # print(client_res.json())

#     # r= request.get('https://api.tu.ac.th')
#     # print('cookie', r.cookies)
#     # cookie = {'res_token' : client_res.json()['access_token']}
#     # new_cook = request.post('https://api.tu.ac.th/', cookie)    
#     # print('new_cook =>' )
#     # print(new_cook.cookies)

#     jar = requests.cookies.RequestsCookieJar()
#     jar.set('access_token', client_res.json() ['access_token'], domain='https://api.tu.ac.th', path='/')
#     r_cookie = requests.post('https://api.tu.ac.th', cookies=jar)

#     print('r_cookie.text', r_cookie)
#     return HttpResponse('<h1>success</h1>')
#     #return JsonResponse(client_res.json())


@csrf_exempt
@parser_classes((JSONParser,))
def redirectURL(request) :
    print('================== redirectURL ==================')
    query_string = request.GET
    code = query_string['code']
    print(query_string)
    print(' code   '+code)
    # client_res = request.get('https://www.google.com/')
    data = {
        'code' : code,
        'client_id' : 'Qzw4Fnulqrb1Mswk9nYUEUi2rHOHeyKClwq2IM1X',
        'client_secret' : 'OSwcfymQOUAG4AqIqe0ZlOR8PUR0V7KgXLaxpT9PLGLLoNO52CrBVEJMDd6g0ACtfLxOLnqFIuHxrH5Ie1L3cRE3TGCXlw35mNhEWXLSMiP94qd6d8X9VZECTi5uAgvO' ,
        'redirect_uri' : 'http://10.75.72.7:8000/api/redirect/tu/' ,
        'grant_type' : 'authorization_code'
    }

    client_res = requests.post('https://api.tu.ac.th/o/token/' , data = data)
    print('============client_res==============')

    print(client_res.json())
    # print(client_res.json()['access_token'])
    # print(client_res.json())

    # r= request.get('https://api.tu.ac.th')
    # r = requests.get('<MY_URI>', headers={'Authorization': 'TOK:<MY_TOKEN>'})
    r = requests.get('https://api.tu.ac.th/api/me/', headers={'Authorization': 'Bearer '+ client_res.json()['access_token']})
    print("test r :")
    print(r)
    print("test r.json :")
    print(r.json())

    # r = requests.get('https://api.tu.ac.th/api/me/', auth=('user', 'pass'))
    # print('cookie', r.cookies)
    # cookie = {'res_token' : client_res.json()['access_token']}
    # new_cook = request.post('https://api.tu.ac.th/', cookie)    
    # print('new_cook =>' )
    # print(new_cook.cookies)
    print("Testtttttt")
    print(r.json()['username'])
    try:
            user = User.objects.get(userid=r.json()['username'])
            # user = request.user
            print("Testtttttt Update data")
            print(r.json()['username'])
            
            data = {
                "userid" : r.json()['username'],
                "firstname" : r.json()['firstname'],
                "lastname" : r.json()['lastname'],
                "major" : r.json()['company'],
                "department" : r.json()["department"]
            }
            serializer = UserSerializer(user,data=data)

            print("***********************************")
            print(serializer)

            if serializer.is_valid():
                print("If Upadate ")
                serializer.save()
            else :
                print("else Upadate ")
                return HttpResponse('<h1> Not success Update</h1>')

            # return HttpResponse(serializer.data)
    except User.DoesNotExist:
            # request.method == 'POST':
            # print('1. test: post request')
            # # print(request)
            # print("Testtttttt")
            print("Testtttttt Add New data")
            
            data = {
                "userid" : r.json()['username'],
                "firstname" : r.json()['firstname'],
                "lastname" : r.json()['lastname'],
                "major" : r.json()['company'],
                "department" : r.json()["department"]
            }
            # data = JSONParser().parse(request)
            # print('2. test: post request')
            # print(data)
            serializer = UserSerializer(data=data)
            print("***********************************")
            print(serializer)
            if serializer.is_valid():
                print("If Add New ")
                
                serializer.save()
            else :
                print("else Add New ")
                
                return HttpResponse('<h1> Not success Add New</h1>')

    

    jar = requests.cookies.RequestsCookieJar()
    jar.set('access_token', client_res.json() ['access_token'], domain='https://api.tu.ac.th', path='/')
    r_cookie = requests.post('https://api.tu.ac.th', cookies=jar)
    
    

    print('r_cookie.text', r_cookie)
    

    response = HttpResponse('<h1>success</h1> <script>setTimeout(() => window.close(), 3000)</script> <script>(function() { setTimeout(function() { window.close() }, 3000) })()</script>')
    # response = HttpResponse('<h1>success</h1>')
    
    response.set_cookie('userid', r.json()['username'])


    return JsonResponse(client_res.json())
    # return response
    #return JsonResponse(client_res.json())
