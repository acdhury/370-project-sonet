from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from post.models import Post
from follow.models import Follow
from .forms import UserUpdateForm, BioUpdateForm, ProfilePictureUpdateForm # Import UserUpdateForm
from .models import Bio  # Import the Bio model


def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profile_user).order_by('-created_at')
    bio = Bio.objects.filter(user=profile_user).first()  # Retrieve the bio if exists

    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

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
        'bio': bio,  # Add the bio to the context
    }
    return render(request, 'account/profile.html', context)

@login_required
def update_name(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your name has been updated.")
            return redirect('account:profile', username=request.user.username)
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'account/update_name.html', {'form': form})


@login_required
def update_bio(request):
    bio, created = Bio.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = BioUpdateForm(request.POST, instance=bio)
        if form.is_valid():
            form.save()
            messages.success(request, "Your bio has been updated.")
            return redirect('account:profile', username=request.user.username)
    else:
        form = BioUpdateForm(instance=bio)

    context = {
        'form': form
    }
    return render(request, 'account/update_bio.html', context)



@login_required
def update_profile_picture(request):
    bio, created = Bio.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfilePictureUpdateForm(request.POST, request.FILES, instance=bio)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile picture has been updated.")
            return redirect('account:profile', username=request.user.username)
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = ProfilePictureUpdateForm(instance=bio)
    
    context = {
        'form': form
    }
    return render(request, 'account/update_profile_picture.html', context)