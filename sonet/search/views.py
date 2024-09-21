from django.shortcuts import render
from django.contrib.auth.models import User
from post.models import Post  # Import your Post model

def search_results(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    users = User.objects.filter(username__icontains=query)  # Search for users
    posts = Post.objects.filter(content__icontains=query)  # Search for posts (replace 'content' with your post's content field)
    
    context = {
        'query': query,
        'users': users,
        'posts': posts,
    }
    return render(request, 'search/results.html', context)
