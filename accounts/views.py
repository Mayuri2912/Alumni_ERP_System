# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required # <-- Make sure this is imported
# Import all your forms
from .forms import AlumniUserCreationForm, AlumniAuthenticationForm, ProfileEditForm 

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

def student_login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard') # Send logged-in users to the dashboard

    login_form = AlumniAuthenticationForm()

    if request.method == 'POST':
        login_form = AlumniAuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('username') # This is the email
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            
            if user is not None:
                # Check if the user is actually a student
                if user.user_type == 'Student':
                    login(request, user)
                    return redirect('dashboard')
                else:
                    login_form.add_error(None, "This login is for students only. Alumni, please use the alumni login page.")
            else:
                login_form.add_error(None, "Invalid email or password.")
    
    context = {
        'login_form': login_form,
    }
    return render(request, 'accounts/student_login.html', context)

# --- !! THIS IS THE NEW VIEW FOR EDITING YOUR PROFILE !! ---
@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard') # Redirect to dashboard after saving
    else:
        form = ProfileEditForm(instance=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'accounts/edit_profile.html', context)