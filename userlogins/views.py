from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Authority
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm



# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # authority = Authority(user=user, name=form.cleaned_data['name'])
            # authority.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'form_template.html', {'form': form,"form_heading":"Registration","button_text":"Register"})

def user_login(request):
    try:
        if request.method == 'POST':
            next = request.GET.get('next')
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    if next:
                        return redirect(next)
                    return redirect('home')
        else:
            form = AuthenticationForm()
        
        return render(request, 'login.html', {'form': form})
    except Exception as e:
        pass

def user_logout(request):
    logout(request)
    return redirect('login')