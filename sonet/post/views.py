from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed:index')  # Redirect to the feed after post creation
    else:
        form = PostForm()
    return render(request, 'post/create_post.html', {'form': form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()  # If already liked, unlike the post
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def comment_on_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = CommentForm()
    
    return render(request, 'post/post_detail.html', {'post': post, 'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Get all comments on this post
    form = CommentForm()
    return render(request, 'post/post_detail.html', {'post': post, 'comments': comments, 'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Ensure only the owner can delete the post
    if request.user == post.user:
        post.delete()
        return redirect('account:profile', username=request.user.username)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Ensure only the owner can update the post
    if request.user != post.user:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('account:profile', username=request.user.username)
    else:
        form = PostForm(instance=post)

    return render(request, 'post/update_post.html', {'form': form})