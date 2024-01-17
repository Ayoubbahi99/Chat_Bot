from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone


openai.api_key = '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'

def ask_openai(message):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-1106',  # Use a valid model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ],
            max_tokens=150,
            n=1,
            stop=None
        )
        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

# Create your views here.
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        chat = Chat(User=request.user, message=message, response=response, created_at=timezone.now)
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, "chatbot.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password1']

        if pass1 == pass2:
            try:
                user = User.objects.create_user(username, email, pass1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                err_message = 'Error creating account'
                return render(request, 'register.html', {'err_message': err_message})
        else:
            err_message = "Password don't match"
            return render(request, 'register.html', {'err_message': err_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect(login)