from django.shortcuts import render, redirect
from post.models import Post, Like, Comment
from follow.models import Follow
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def feed(request):
    user = request.user

    # Get the list of users that the current user is following
    followed_users = Follow.objects.filter(follower=user).values_list('following', flat=True)

    # Retrieve the posts made by the user and the users they follow, sorted by creation time
    posts = Post.objects.filter(Q(user=user) | Q(user__in=followed_users)).order_by('-created_at')

    # For each post, check if the current user has liked it
    for post in posts:
        post.is_liked = Like.objects.filter(user=user, post=post).exists()

    # Retrieve the actual user objects for the left section
    followed_users_objects = Follow.objects.filter(follower=user).select_related('following')

    # Handle liking a post
    if request.method == "POST" and 'like_post_id' in request.POST:
        post_id = request.POST.get('like_post_id')
        post = Post.objects.get(id=post_id)
        liked = Like.objects.filter(user=user, post=post).exists()
        if liked:
            Like.objects.filter(user=user, post=post).delete()
        else:
            Like.objects.create(user=user, post=post)
        return redirect('feed:index')

    # Handle adding a comment to a post
    if request.method == "POST" and 'comment_post_id' in request.POST:
        post_id = request.POST.get('comment_post_id')
        comment_content = request.POST.get('comment_content')
        post = Post.objects.get(id=post_id)
        if comment_content:
            Comment.objects.create(user=user, post=post, content=comment_content)
        return redirect('feed:index')

    context = {
        'posts': posts,
        'followed_users': followed_users_objects,
    }

    return render(request, "feed/index.html", context)


