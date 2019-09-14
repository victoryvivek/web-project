from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django import forms

from firstapp.forms import LoginForm,UserRegisterForm,AnswerForm
from firstapp.models import UserInfo,Question

# Create your views here.

def login_user(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                user_info=get_object_or_404(UserInfo, user_id=user.pk)
                return redirect('firstapp:dashboard',current_level=user_info.current_level,rank=user_info.rank)
    else:
        form=LoginForm()
    return render(request,'login.html',{'form':form})

def register_user(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            password_ = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email_ = form.cleaned_data['email']
            user = User.objects.create_user(username=user_name, email=email_, password=password_, first_name=first_name, last_name=last_name)
            user.save()
            user_info=UserInfo.create(user)
            user_info.save()
            return redirect('firstapp:login')
    else:
        form = UserRegisterForm()
    return render(request,'registration.html',{'form':form})

def go_to_dashboard(request,current_level,rank):
    user_info=get_object_or_404(UserInfo, user_id=request.user.pk)
    if current_level == user_info.current_level and rank==user_info.rank:
        return render(request,'dashboard.html',{'current_level':current_level,'rank':rank})
    else:
        return redirect('firstapp:dashboard',current_level=user_info.current_level,rank=user_info.rank)

def logout_user(request):
    logout(request)
    return redirect('firstapp:thanks')

def thanks_for_logging(request):
    return render(request,'thanks_for_logging.html')

def go_to_question(request,q_no):

    user_info=get_object_or_404(UserInfo, user_id=request.user.pk)
    current_level=user_info.current_level

    if q_no != current_level:
        return redirect('firstapp:question_current',q_no=current_level)

    question_obj=Question.objects.filter(question_no=current_level)
    for i in question_obj:
        heading=i.heading
        img=i.product_image
        question_no=i.question_no
        question_answer=i.question_answer

    if request.method=="POST":
        form=AnswerForm(request.POST)
        if form.is_valid():
            answer=form.cleaned_data['answer']

            if answer==question_answer:
                user_info.current_level=user_info.current_level+1
                user_info.score=user_info.score+1
                user_info.save()
                if user_info.score==25:
                    return redirect('firstapp:complete_task')
                return redirect('firstapp:question_current',q_no=user_info.current_level)
            else :
                return render(request,'level1.html',{'heading':heading,'img':img,'question_no':question_no,'form':form,'wrong':True,'current_level':current_level})           
            
    else:
        form=AnswerForm()
    return render(request,'level1.html',{'heading':heading,'img':img,'question_no':question_no,'form':form,'wrong':False,'current_level':current_level})

def complete_task(request):
    return render(request,'complete_task.html')

def get_leaderboard(request):

    user_info=get_object_or_404(UserInfo, user_id=request.user.pk)
    current_level=user_info.current_level

    user_info_queryset=UserInfo.objects.all()

    user_info_list=[]

    for x in user_info_queryset:
        user_info_list.append(x)

    user_info_list.sort(key=get_score, reverse=True)
    
    cnt=1
    for x in user_info_list:
        x.rank=cnt
        cnt=cnt+1

    return render(request,'leaderboard.html',{'user_info_list':user_info_list,'current_level':current_level})

def get_score(user_info):
    return user_info.score

def index(request):
    return render(request,'preneur.html')

def home(request):
    user_info=get_object_or_404(UserInfo, user_id=request.user.pk)
    current_level=user_info.current_level
    return render(request,'homeredirect.html',{'current_level':current_level})
