# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from demoapp.forms import SignUpForm,Log_in_Form,Postform,Like_Unlike,Commentform
from demoapp.models import UserModel,Sesseion_token,Post_Model,Like_Model,Comment_Model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from imgurpython import ImgurClient
from django_project.settings import BASE_DIR

# Create your views here.


def signup_view(request):
    dictionary = {}
    if request.method == "GET" :
        signup_form = SignUpForm()
        dictionary['signup'] = signup_form
        return render(request,"signup_1.html" , dictionary)
    elif request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form:
            if signup_form.is_valid():
                username = signup_form.cleaned_data.get('username')
                name = signup_form.cleaned_data.get('name')
                email = signup_form.cleaned_data.get('email')
                password = signup_form.cleaned_data.get('password')
                while len(username) < 5:
                    dictionary['invalid_username']="*Username must be atleast 5 chars*"
                    return render(request, "signup_1.html", dictionary)
                while len(password) < 5:
                    dictionary['invalid_pass'] = "*Password must be atleast 5 chars*"
                    return render(request, "signup_1.html", dictionary)
                #save user to DATABASE...
                user = UserModel(name = name,username=username,email=email,password=make_password(password))
                user.save()
                dictionary['registered'] = signup_form
                return render(request, "registered.html", dictionary)
            else :
                dictionary['invalid'] = "Invalid values, plzz enter again"
                return render(request, "signup_1.html", dictionary)
        else:
            log_in(request)




def log_in(request):
    dictionary = {}
    if request.method == "GET" :
        #login = Log_in_Form()
        #dictionary['form'] = login
        template_name = "log_in.html"
    elif request.method == "POST" :
        login = Log_in_Form(request.POST)
        if login.is_valid() :
            username = login.cleaned_data['username']
            password = login.cleaned_data['password']
            user = UserModel.objects.filter(username=username).first()
            if user :
                # Check for the password
                if check_password(password, user.password):
                    token = Sesseion_token(user = user)
                    token.create_token()
                    token.save()
                    response = redirect("/home/")
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else :
                    dictionary['invalid'] = 'invalid Password..'
                    template_name = "log_in.html"


            else :
                return redirect("/")
        else :
            dictionary['invalid_password'] = 'Invalid *User-name or *Password..'
            template_name = "log_in.html"

    return render(request, template_name, dictionary)

def check_auth(request):
    if request.COOKIES.get("session_token"):
        session = Sesseion_token.objects.filter(session_token = request.COOKIES.get('session_token')).first()
        if session :
            return session.user
        else :
            return None


def like_post(request):
    user = check_auth(request)
    #dictionary = {}
    if user == None:
        return redirect('/login/')
    elif user and request.method == "POST":
        form = Like_Unlike(request.POST)
       #****** ERRor*************
        if form.is_valid():
            post_id = form.cleaned_data.get("post").id
            existing_like = Like_Model.objects.filter(post_id=post_id, user=user).first()

            if  existing_like == None:
                Like_Model.objects.create(post_id=post_id, user=user)
                #post = Post_Model.objects.filter(id=post_id).first()
                #post.has_liked = True
                #post.save()
            else:
                existing_like.delete()
                #post = Post_Model.objects.filter(id=post_id).first()
                #post.has_liked = False
                #post.save()
            return redirect("/home/")
            #*****ERROR****#
        else:
            return redirect('/feed/')
    else:
        return  redirect("/login/")


def homepage(request):
    user = check_auth(request)
    if user and request.method == "GET":
        posts = Post_Model.objects.all().order_by("created_on")
        #check current user liked the post or not
        for post in posts:
            existing_like = Like_Model.objects.filter(post = post.id, user = user)
            if existing_like:
                post.has_liked = True

        return render(request,"home.html",{"posts":posts})
    #elif user and request.method == "POST":
        #like_post(request)



def feed_back(request):
    dict = {}
    user = check_auth(request)
    if user == None:
        return redirect("/login/")
    else :
        if request.method == "GET":
            form = Postform()
            return render(request,"post.html",{'form':form})
        elif request.method == "POST":
            form = Postform(request.POST,request.FILES)
            if form :
                if form.is_valid():
                        image = form.cleaned_data.get('image')
                        caption = form.cleaned_data.get('caption')
                        post = Post_Model(user=user, image=image, caption=caption)
                        post.save()
                        image = post.image.url
                        path = str(BASE_DIR +"\\"+ image)
                        client = ImgurClient("9833d69a08cef7e", "f1603dd86bfe25b3f73427309b0561a92ff54262")
                        post.image_url = client.upload_from_path(path, anon=True)['link']
                        post.save()
                        print(post.image_url)
                        return redirect("/home/")
                else:
                        dict['no_post'] = "Please choose a file , Caption is Mandatory...."
                        return render(request,"post.html",dict)




def comment_view(request):
    user = check_auth(request)
    if user == None:
        return redirect("/login/")
    elif user and request.method == "POST":
        form = Commentform(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get("post").id
            curr_post = Post_Model.objects.filter(id=post_id).first()
            comment_text = form.cleaned_data.get("comment_text")
            comment = Comment_Model.objects.create(user=user, post= curr_post, comment_text=comment_text)
            comment.save()
            return redirect("/home/")
        else:
            return redirect("/home")
    else:

        return redirect("/login/")



            #elif request.method =="POST":
def log_out(request):
            user_id = check_auth(request)
            delete_user = Sesseion_token.objects.filter(user = user_id)
            delete_user.delete()
            return redirect("/signup/")


