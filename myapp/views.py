from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from myapp.models import Post
from cloudinary.uploader import upload

import logging
logger = logging.getLogger('django')

def home_view(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    else:
        return redirect('login')

@login_required
def post_list(request):
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    query = request.GET.get('q', '')

    if query:
        posts = posts.filter(title__icontains=query)

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    print(page_objs.paginator.object_list.count())

    return render(request, 'myapp/post_list.html', {'page_objs': page_objs, 'query': query})

@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if image:
            try:
                logger.debug(f"Uploading image: {image.name}")
                response = upload(image, resource_type="image")
                image_url = response['url']
                logger.debug(f"Upload completed, image url: {image_url}")

                Post.objects.create(title=title, content=content, user=request.user, image=image_url)
            except Exception as e:
                logger.error(f"Error uploading image: {e}")
        else:
            logger.debug("No image found in the request.")

        return redirect('post_list')

    return render(request, 'myapp/create_post.html')

@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        post.title = title
        post.content = content

        if image:
            post.image = image

        post.save()

        return redirect('post_list')

    return render(request, 'myapp/post_detail.html', {'post': post})

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        if post:
            post.delete()

        return redirect('post_list')

    return render(request, 'myapp/delete_post.html', {'post': post})

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is existed.')

        if password == confirm_password:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('post_list')
        else:
            messages.error(request, 'Password and Confirm Password is not matched.')

    return render(request, 'myapp/signup.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('post_list')
        else:
            messages.error(request, 'Username or password is wrong.')

    return render(request, 'myapp/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')
