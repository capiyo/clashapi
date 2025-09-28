from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import  requests
from django.views.decorators.csrf import csrf_exempt
from .utils import createUser, login_user,getGames, getUserDetails,postMessage,add_pledges,get_pledges
from rest_framework.decorators import api_view


# Create your views here.

@api_view(['POST'])
def register(request):
    print("Hellloooooooo")
    return createUser(request)



@api_view(['POST'])
def pledging(request):
    return add_pledges(request)
@api_view(["GET"])
def getPlegdges(request):
    return get_pledges(request)


@api_view(['GET'])
def getAllGames(request):
    print("Hellloooooooo")
    return getGames(request)

""""def postgig(request):
    if request.method == 'POST':
        print("Capiyo request received")
    else:print("Not so coollll")    
    return creategig(request)
    """



@api_view(['POST'])
def posMessage(request):
    print("Capiyo")
   # response = requests.post(url="https://example.com/", data="<some_data>")
    return  postMessage(request)

@api_view(['POST'])
def postProfile(request):
    print("Capiyo")
   # response = requests.post(url="https://example.com/", data="<some_data>")
    return  createProfile(request)








"""def postgig(request):
   
    form = JobForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()

    if request.method == 'POST':

        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(
                    request, 'You are successfully posted your job! Please wait for review.')
            return redirect(reverse("jobapp:single-job", kwargs={
                                    'id': instance.id
                                    }))

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'jobapp/post-job.html', context)
"""









@api_view(['POST', 'OPTIONS'])
def loginUser(request):
    if request.method == "POST":
        return login_user(request)
    elif request.method == "OPTIONS":
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, X-CSRFToken'
        response['Access-Control-Max-Age']= '3600'
        return response

@api_view(["GET"])
def getMyDetails(request):
    print("Am getiing your details")
    return getUserDetails(request)

@api_view(["GET"])
def logout(request):    
    return logoutUser(request)



@api_view(["GET"])
def gigs(request):
    return getGigs(request)


def index(request):
    return render(request, 'index.html', {})

@api_view(["POST", "OPTIONS"])
def approve(request):
    print("Hello world")
    if request.method == "POST":
        return approveUser(request) 
    elif request.method == "OPTIONS":
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, X-CSRFToken'
        response['Access-Control-Max-Age']= '3600'
        return response