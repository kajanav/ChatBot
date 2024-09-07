from django.shortcuts import render
from django.http import JsonResponse
import openai
import os
from django.contrib.auth.models import AnonymousUser
from .models import Chat
from django.utils import timezone
from groq import Groq

openai_api_key = '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'
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer

def chatbot(request):
    if isinstance(request.user, AnonymousUser):
        chats = Chat.objects.none()
    else:
        chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        # Save the chat interaction in the database
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()

        return JsonResponse({'message': message, 'response': response})

    return render(request, 'chatbot.html', {'chats': chats})
