from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.contrib.auth.models import AnonymousUser


from .models import Chat

from django.utils import timezone


openai_api_key = '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'
openai.api_key = openai_api_key

def ask_openai(message):
   response = openai.ChatCompletion.create(
     model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
   )
   answer = response['choices'][0]['message']['content'].strip()
   return answer
# Create your views here.
def chatbot(request):
    if isinstance(request.user, AnonymousUser):
        chats = Chat.objects.none()
    else:    
        chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})


