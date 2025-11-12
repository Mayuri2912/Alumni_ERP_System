from django.shortcuts import render

# Create your views here.
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import AlumniUserCreationForm, AlumniAuthenticationForm 

def login_signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    login_form = AlumniAuthenticationForm() 
    signup_form = AlumniUserCreationForm()

    if request.method == 'POST':
        if 'submit_login' in request.POST:
            login_form = AlumniAuthenticationForm(request, data=request.POST) 
            if login_form.is_valid():
                email = login_form.cleaned_data.get('username') # This is the email
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
        
        elif 'submit_signup' in request.POST:
            signup_form = AlumniUserCreationForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect('dashboard')

    context = {
        'login_form': login_form,
        'signup_form': signup_form,
    }
    return render(request, 'accounts/login_signup.html', context)

def logout_view(request):
    logout(request)
    return redirect('login_signup')