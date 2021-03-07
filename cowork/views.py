from django.shortcuts import redirect, render

from .forms import CommentForm
from .models import Comment


def comments(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save()
            return redirect('comments')
    else:
        comment_form = CommentForm()
    comments = Comment.objects.all().order_by('-create_time')
    return render(
        request,
        'cowork/comments.html',
        {'comment_form': comment_form, 'comments': comments},
    )
