# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
#from .models import Weather
from django.http import JsonResponse
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import sys
from django.contrib.auth.forms import PasswordChangeForm
from flask_socketio import SocketIO, send, emit                                 
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.
def check(request):
    return render(request,"slidercheck.html")

def home(request):
	return render(request,"home.html")

def show_add_page(request):
	return render(request,"add_page.html")

# MARK : main page
from .models import Post
from .forms import myForm

web_name = "Library"
path_link = [ 	{'name':"HOME",'link':"/" }]
				#{'name':"LOGIN",'link':"/signin" }]

def add_page(request):
    if request.method == 'POST':
        form = myForm(request.POST or None)
        #form = myForm(request.POST)
        if form.is_valid():
            Class   = form.cleaned_data['Class']
            subject = form.cleaned_data['subject']
            lesson  = form.cleaned_data['lesson']
            chapter = form.cleaned_data['chapter']
            detail  = form.cleaned_data['detail']
            #publish = form.cleaned_data['publish']
            out = Class+" : "+subject+" : "+lesson+" : "+chapter+" : "+detail#+" : "+("True" if publish else "False")
            post = Post()
            post.Class    = Class
            post.subject  = subject
            post.lesson   = lesson
            post.chapter  = chapter
            post.detail   = detail
            post.author   = request.user
            post.created_date = timezone.now()
            post.publish  = True
            post.view     = 0
            post.save()
            print(post.detail)
            return HttpResponse(out, content_type='text/plain')
            #return redirect('class_page')

            #return HttpResponse(out, content_type='text/plain')
            #return redirect('class_page')

    else:
        form = myForm()
    return render(request,"page/add_detail.html",{
        'path_link':path_link,
        'web_name':web_name,
        'form':form
        })

def class_page(request):
    data = Post.objects.all()
    class_title = []
    for i in data :
        haved = False
        for j in class_title:
            if i.Class == j:
                haved = True
        if haved == False:
            class_title.append(i.Class)
    return render(request,"page/class_page.html",{
        'class_title':class_title,
        'path_link':path_link,
        'web_name':web_name
        #'class_data':class_data
        })

def add_class(request):
    #if request.method == 'POST':
        
        #aClass = Post(title=text,author=request.user)
        #aDetail = SDetail(textType=0)
        #aDetail.save()
        #aChapter = Chapter(author=request.user,detail=aDetail)
        #aChapter.save()
        #aLesson = Lesson(title="",chapter=aChapter)
        #aLesson.save()
        #aSubject = Subject(title="test2NaJa",lesson=aLesson)
        #aSubject.save()
        #aClass = Class.objects.get(title="test") #Class(title=text,subject=aSubject)
        #aClass.save()
    return render(request,"page/add_class.html")

def add_detail(request):
    return render(request,"page/add_detail.html")


# MARK : Add contain -----------------------------------------------------------------------------------

from django.shortcuts import redirect
from .forms import PostForm

from django.utils import timezone


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            #return redirect('post_detail', pk=post.pk)
            #return HttpResponse("Saved", content_type='text/plain')
            return redirect('post_new')
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


# MARK : Login method

def signup(request):
    if request.method == 'POST' and 'username' in request.POST:
        form = UserCreationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['Check_password']
        email = request.POST['Email']
        fullname = request.POST['Fullname']
        lastname = request.POST['Lastname']
        if password==password2:
            user = authenticate(username=username, password=password)
            if user is not None:
                return redirect('singup')
            else:
                print password
                print username
                print user
                password1 = password
                #return redirect('signin')
                user = User.objects.create_user(
                    username=username,
                    password=password1,
                    email=email,
                    first_name=fullname,
                    last_name=lastname,
                    )
                return redirect('class_page')  
        else:
            print "UnmatchPassword"    
    else:
        form = UserCreationForm()
    return render(request, 'signup2.html', {'form': form})
def signin(request):
	if request.method == 'POST' and 'username' in request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		print >>sys.stderr, "debug"
		if user is not None:
			if user.is_active:

				if 'remember' in request.POST:
					print>>sys.stderr, "%s type: %s"%(request.POST['remember'],type(request.POST['remember']))
					if request.POST['remember']=='1':
						request.session.set_expiry(604800) #remember keep session for a week
				else:
					request.session.set_expiry(14400) #not remember keep session for 4hrs
				print >>sys.stderr, "session expiry: %s"%request.session.get_expiry_age()

				login(request, user)
				if 'username' in request.session:
					print >>sys.stderr, "username_i: %s"%request.session['username']
				request.session['username'] = user.username
				print >>sys.stderr, "username_f: %s"%request.session['username']
				
				return redirect('class_page')
			else:
				msg="Disabled account"
		else:
			msg="Invalid username or password"
		return render(request,'login.html',{'msg': msg})   
	return render(request,'login.html',{'msg': ""})

def signout(request):
	print "signout"
	if 'username' in request.session:
		del request.session['username']
		print "del uname"
	logout(request)
	return redirect('class_page')

@login_required(login_url='signin')

def change_password(request):
    form = PasswordChangeForm(user=request.user)
    print >>sys.stderr, "request.user: %s"%request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('class_page')

    return render(request, 'change_password.html', {
        'form': form,
    })

#Mark : Upload Method

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form
    })





