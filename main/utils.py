import smtplib, ssl
from .models import Users,PostMessage,Pledges,Fixtures
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer,PledgesSerializer,FixturesSerializer

# from django.shortcuts import render   





def createUser(request):
    phone = request.data['phone']
    password = request.data['password']
    email = request.data['username']
    

    user = Users.objects.create_user(email=email, password=password, phone=phone)
    print(user)
    if user:
        login_user(request)
        return JsonResponse({"isLogged": True})
    return JsonResponse({"isLogged": False})




def getGames(request):
    print("Am reached")
    if request.user.is_authenticated:
        data =Fixtures.objects.all()    
        serializer_data =FixturesSerializer(instance=data, many=True)
        
        
        return JsonResponse(serializer_data.data,)
    else:    
        data =Fixtures.objects.all()                
        # i need to scrape
        #and i need to return games while scraping
        
        
        
        
        serializer_data = FixturesSerializer(instance=data, many=True)
        return JsonResponse(serializer_data.data, safe=False)
        #return JsonResponse({"error": "User is not authenticated"})
    
    
def getUserDetails(request):
    print("Capiyo hellooooo")

    if request.user.is_authenticated:
        print("User Is authenticated")
        user = request.user
        serialized_data = UserSerializer(user)
        return JsonResponse(serialized_data.data)
    else:    
        return JsonResponse({"error": "User is not authenticated"})
def get_pledges(request):
    print("Capiyo hellooooo")

    if request.user.is_authenticated:
         data =Pledges.objects.all()    
         serializer_data = PledgesSerializer(instance=data, many=True)
         print(data)
        
         return JsonResponse(serializer_data.data,)
    else:    
         data =Pledges.objects.all()    
         serializer_data = PledgesSerializer(instance=data, many=True)
         print(data)
        
         return JsonResponse(serializer_data.data, safe=False)
def add_pledges(request):
    homeTeam=request.data['homeTeam']    
    awayTeam=request.data['awayTeam']
    progress=request.data['progress']
    placed=request.data['placed']
    amount=request.data['amount']
    date=request.data['date']
    day=request.data['day']
    option=request.data['option']
    pledger=request.data['pledger']
    placer=request.data['placer']
    outcome=request.data['outcome']
    
    pledge =Pledges.objects.create(homeTeam=homeTeam,awayTeam=awayTeam,progress=progress,placed=placed
                                   ,amount=amount,date=date,day=day,option=option,pledger=pledger,placer=placer,outcome=outcome)
    if(pledge):
        print("Saved")
   # gig.save()
    #print(title,deadline,budget,giginfo)
    return JsonResponse({"isLogged": False})

    



def postMessage(request):
    
    message = request.data['message']
    senderid= request.data['senderid']
    receiverid=request.data['receiverid']
    time=request.data['time']
    
    
    

    message =PostMessage.objects.create(message=message,senderid=senderid,receiverid=receiverid,time=time)
    if(message):
        print("Saved")
   # gig.save()
    #print(title,deadline,budget,giginfo)
    return JsonResponse({"isLogged": False})


   







def login_user(request):

    email= request.data['username']
    
    password = request.data['password']
    print(email, password)
    user = authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user=user)
        request.session.save()
        
        return JsonResponse({"isLogged": True})
    else:
        return JsonResponse({'error': "User does not exist", "isLogged": False})
    
    


    
def getUserDetails(request):
    print("Capiyo hellooooo")

    if request.user.is_authenticated:
        print("User Is authenticated")
        user = request.user
        serialized_data = UserSerializer(user)
        return JsonResponse(serialized_data.data)
    else:    
        return JsonResponse({"error": "User is not authenticated"})

def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"isLoggedOut": True})
    return JsonResponse({"isLoggedOut": False, "error": "Error while loging the user"})


    


