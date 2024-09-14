from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from post.models import Post
from follow.models import Follow

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profile_user).order_by('-created_at')

    # Check if the current user follows the profile user
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    # Handle follow/unfollow action
    if request.method == 'POST':
        if is_following:
            Follow.objects.filter(follower=request.user, following=profile_user).delete()
        else:
            Follow.objects.create(follower=request.user, following=profile_user)
        return redirect('account:profile', username=username)

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
    }
    return render(request, 'account/profile.html', context)
