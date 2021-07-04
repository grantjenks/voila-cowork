from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
from .models import Document, Topic, Comment


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            return HttpResponse(user.username)
    return HttpResponse(request.user.username)


def logout(request):
    auth_logout(request)
    return HttpResponse('OK')


def comments(request, author, document, topic):
    kwargs = {}

    author, _ = User.objects.get_or_create(username=author)
    kwargs['author'] = author
    document, _ = Document.objects.get_or_create(name=document, author=author)
    kwargs['document'] = document
    topic, _ = Topic.objects.get_or_create(name=topic, document=document)
    kwargs['topic'] = topic

    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                login(request, form.get_user())
                return redirect(
                    'comments',
                    author=author.username,
                    document=document.name,
                    topic=topic.name,
                )
        else:
            form = AuthenticationForm()
    else:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect(
                'comments',
                author=author.username,
                document=document.name,
                topic=topic.name,
            )
        else:
            form = CommentForm(initial={
                'document': document,
                'topic': topic,
                'author': request.user,
            })

    kwargs['form'] = form
    comments = list(Comment.objects.order_by('-create_time')[:5])
    kwargs['comments'] = comments
    return render(request, 'cowork/comments.html', kwargs)
