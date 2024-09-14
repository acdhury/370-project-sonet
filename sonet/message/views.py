from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from django.db import models

@login_required
def message_list(request):
    # Retrieve users that the current user follows
    users = request.user.following.all()  # Assuming you have a follow field or method
    return render(request, "message/message_list.html", {'users': users})

@login_required
def chat(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    
    # Get all messages between the logged-in user and the recipient
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(recipient=recipient)) |
        (models.Q(sender=recipient) & models.Q(recipient=request.user))
    ).order_by('timestamp')

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(sender=request.user, recipient=recipient, content=content)
            return redirect('message:chat', recipient_id=recipient.id)

    return render(request, "message/chat.html", {'chat_user': recipient, 'messages': messages})
