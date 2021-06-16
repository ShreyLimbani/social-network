from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import json
from .models import User, RELATIONSHIP_FOLLOWING, RELATIONSHIP_BLOCKED, Post, Like, Relationship
from flask.json import jsonify
from django.core.paginator import Paginator


def index(request):
    posts = Post.objects.order_by('timestamp').reverse()
    paginator = Paginator(posts, 10) # Show 10 posts per page.
    try:
        page_number = request.GET.get('page')
    except:
        page_number = 1
    page_obj = paginator.get_page(page_number)    
    return render(request, "network/index.html", {'posts':page_obj})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def following_view(request):
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.get(username = username)
        following = user.get_following()
        posts = Post.objects.filter(poster__in = following).order_by('timestamp').reverse()
        paginator = Paginator(posts, 10) # Show 10 posts per page.
        try:
            page_number = request.GET.get('page')
        except:
            page_number = 1
        page_obj = paginator.get_page(page_number)
        return render(request, 'network/following.html', {'posts':page_obj})
    else:
        return HttpResponseRedirect(reverse('index'))


def profile_view(request, user_id):
    person = User.objects.get(pk=user_id)
    posts = person.post.order_by('timestamp').reverse()
    paginator = Paginator(posts, 10) # Show 10 posts per page.
    try:
        page_number = request.GET.get('page')
    except:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    print(request.get_full_path())
    return render(request, "network/profile.html",{"person":person, "posts":page_obj})


def follow(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            to_user = User.objects.get(pk=request.POST.get('to_user'))
            from_user = User.objects.get(pk=request.user.pk)
            from_user.add_relationship(to_user,RELATIONSHIP_FOLLOWING)

            return HttpResponseRedirect(reverse(profile_view, kwargs = {'user_id':request.POST.get('to_user')}))
    else:
        return HttpResponseRedirect(reverse("index"))


def unfollow(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            to_user = User.objects.get(pk=request.POST.get('to_user'))
            from_user = User.objects.get(pk=request.user.pk)
            relationship = Relationship.objects.get(from_user = from_user, to_user=to_user)
            relationship.delete()
            return HttpResponseRedirect(reverse(profile_view, kwargs = {'user_id':request.POST.get('to_user')}))
    else:
        return HttpResponseRedirect(reverse("index"))


def like(request):
    if request.user.is_authenticated:
        post_id = int(request.body[8:])
        post = Post.objects.get(pk = post_id)
        liker = User.objects.get(pk=request.user.pk)
        like = post.like(liker)        
        like_count = post.likes.count()
        return HttpResponse(content = json.dumps({'count':like_count,'message':'Post Liked'}))
    else:
        return HttpResponse(content = json.dumps({'message':'Sign In First'}))


def removelike(request):
    if request.user.is_authenticated:
        post_id = int(request.body[8:])
        post = Post.objects.get(pk = post_id)
        liker = User.objects.get(pk=request.user.pk)
        like = Like.objects.get(post=post, user=liker)
        like.delete()         
        like_count = post.likes.count()
        return HttpResponse(content = json.dumps({'count':like_count,'message':'Post Unliked'}))
    else:
        return HttpResponse(content = json.dumps({'message':'Sign In First'}))


def add_post(request):
    if request.method == "POST":
        poster = User.objects.get(pk=request.user.pk)
        poster.add_post(request.POST.get('content'))

        return HttpResponseRedirect(reverse(index))

def edit_post(request, post_id):
    if request.user is not None:
        post = Post.objects.get(pk = post_id)
        if post.poster == request.user:
            return render(request, 'network/edit.html', {'post':post})
        else:
            return HttpResponseRedirect(reverse(index))
    else:
            return HttpResponseRedirect(reverse(index))


def save_post(request, post_id):
    if request.user is not None:
        if request.method == "POST":
            post = Post.objects.get(pk=post_id)
            post.content = request.POST.get('content')
            post.save()
            return HttpResponseRedirect(reverse(profile_view, kwargs = {'user_id':request.user.pk}))
        else:
            return HttpResponseRedirect(reverse(index))
    else:
        return HttpResponseRedirect(reverse(index))