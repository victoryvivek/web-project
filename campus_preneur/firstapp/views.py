from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages

from firstapp.forms import LoginForm,UserRegisterForm
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
    return render(request,'dashboard.html',{'current_level':current_level,'rank':rank})

def logout_user(request):
    logout(request)
    return redirect('firstapp:thanks')

def thanks_for_logging(request):
    return render(request,'thanks_for_logging.html')

def go_to_question(request,q_no):
    
    user_info=get_object_or_404(UserInfo, user_id=request.user.pk)
    current_level=user_info.current_level
    question_obj=Question.objects.filter(question_no=current_level)
    for i in question_obj:
        heading=i.heading
        img=i.product_image
        question_no=i.question_no
    return render(request,'level1.html',{'heading':heading,'img':img,'question_no':question_no})
