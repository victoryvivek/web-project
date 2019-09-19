from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django import forms

from firstapp.forms import LoginForm,UserRegisterForm,AnswerForm
from firstapp.models import UserInfo,Question

import requests
import json
import datetime

# Create your views here.

def login_user(request):
    
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        secret_key = "6LfyY7gUAAAAACHtVWYfO5OpHJIBoZ0f2FnzRqho"
        client_key = request.POST.get('g-recaptcha-response')
        captcha_data={
            'secret':secret_key,
            'response':client_key
        }

        get_response_of_user = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',data=captcha_data)

        json_response=json.loads(get_response_of_user.text)
        verify_user = json_response['success']
        print(json_response)
        print("response is " +str(verify_user))

        if user is not None and verify_user==True:
            login(request, user)
            user_info=get_object_or_404(UserInfo, user_id=user.pk)
            #return redirect('firstapp:commingsoon')
            return redirect('firstapp:dashboard',current_level=user_info.current_level,rank=user_info.rank)
        elif user is None :
            messages.error(request, 'Username or Password not Correct')
            return redirect('firstapp:login')
        else :
            messages.error(request, 'Verify reCAPTCHA')
            return redirect('firstapp:login')

    return render(request,'login.html')

def register_user(request):
    if request.method=='POST':
        user_name = request.POST['username']
        password_ = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email_ = request.POST['email']
        college_name=request.POST['college_name']
        user = User.objects.create_user(username=user_name, email=email_, password=password_, first_name=first_name, last_name=last_name)
        user.save()
        user_info=UserInfo.create(user)
        user_info.college_name=college_name
        user_info.save()
        return redirect('firstapp:login')
    return render(request,'registration.html')

def go_to_dashboard(request,current_level,rank):

    if not request.user.is_authenticated:
        return redirect('firstapp:login')

    user_info=get_object_or_404(UserInfo, user_id=request.user.pk)
    if current_level == user_info.current_level and rank==user_info.rank:
        return render(request,'dashboard.html',{'current_level':current_level,'rank':rank})
    else:
        return redirect('firstapp:dashboard',current_level=user_info.current_level,rank=user_info.rank)

def logout_user(request):
    logout(request)
    return redirect('firstapp:thanks')

def thanks_for_logging(request):
    if not request.user.is_authenticated:
        return redirect('firstapp:login')
    return render(request,'thanks_for_logging.html')

def go_to_question(request,q_no):

    if 'val' in request.POST:
        print('post')
    elif 'val' in request.GET:
        val=request.GET['val']
        print('get '+str(val))
    else:
        print('Not Found request')

    if not request.user.is_authenticated:
        return redirect('firstapp:login')

    user_info=get_object_or_404(UserInfo, user_id=request.user.pk)
    current_level=user_info.current_level
    rank=user_info.rank

    if q_no != current_level:
        return redirect('firstapp:question_current',q_no=current_level)

    question_obj=Question.objects.filter(question_no=current_level)
    for i in question_obj:
        heading=i.heading
        img=i.product_image
        question_no=i.question_no
        question_answer=i.question_answer
        image_comments=i.image_comments

    print("in the method")

    if request.method=="POST":
    
        answer=request.POST['answer']
        print("answer", answer)

        if answer==question_answer:
            user_info.current_level=user_info.current_level+1
            user_info.score=user_info.score+1
            user_info.timestamp=datetime.datetime.now()
            user_info.save()
            if user_info.score==25:
                return redirect('firstapp:complete_task')
            return redirect('firstapp:question_current',q_no=user_info.current_level)
        else :
            return render(request,'level1.html',{'heading':heading,'img':img,'question_no':question_no,'wrong':True,
                                                 'current_level': current_level, 'image_comments': image_comments, 'rank': rank})
            
   
    return render(request, 'level1.html', {'heading': heading, 'img': img, 'question_no': question_no, 'wrong': False, 
                                           'current_level': current_level, 'image_comments': image_comments, 'rank': rank})

def complete_task(request):
    if not request.user.is_authenticated:
        return redirect('firstapp:login')
    return render(request,'complete_task.html')

def get_leaderboard(request):

    if not request.user.is_authenticated:
        return redirect('firstapp:login')

    user_info=get_object_or_404(UserInfo, user_id=request.user.pk)
    current_level=user_info.current_level
    rank=user_info.rank

    user_info_queryset=UserInfo.objects.all()

    user_info_list=[]

    for x in user_info_queryset:
        user_info_list.append(x)

    user_info_list.sort(key=get_timestamp)
    user_info_list.sort(key=get_score, reverse=True)
    
    cnt=1
    for x in user_info_list:
        x.rank=cnt
        cnt=cnt+1

    return render(request,'leaderboard.html',{'user_info_list':user_info_list,'current_level':current_level,'rank':rank})

def get_score(user_info):
    return user_info.score

def get_timestamp(user_info):
    return user_info.timestamp

def index(request):
    return render(request,'preneur.html')

def home(request):
    
    if request.user.is_authenticated :
        user_info=get_object_or_404(UserInfo, user_id=request.user.pk)
        current_level=user_info.current_level
        rank=user_info.rank
    else:
        current_level=1
        rank=1
    return render(request,'homeredirect.html',{'current_level':current_level,'rank':rank})

def go_to_developers(request):
    return render(request,'developers.html')

def comming_soon(request):
    return render(request,'commingsoon.html')

def contact(request):
    return render(request,'contact.html')

def rules(request):
    return render(request,'rules.html')
