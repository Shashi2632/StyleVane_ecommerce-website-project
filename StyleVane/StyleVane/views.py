from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            return redirect('index')  # Redirect to the home page or another page after login.
        else:
            # If authentication fails, display an error message
            error_message = "Invalid username or password. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.create_user(username, email, password)
            login(request, user)  # Log the user in after signup
            return redirect('index')  # Redirect to the home page or another page after signup.
        except Exception as e:
            # Handle the exception (e.g., display an error message or redirect to an error page)
            return render(request, 'login.html', {'error_message': str(e)})

    return render(request, 'login.html')

def logout_view(request):
    # Log out the user from the current session
    logout(request)

    if request.session is not None and request.session.session_key is not None:
        # Clear all sessions for the user
        Session.objects.filter(session_key__startswith=request.session.session_key[:8]).delete()

    return redirect('login')  # Redirect to the login page after logout.