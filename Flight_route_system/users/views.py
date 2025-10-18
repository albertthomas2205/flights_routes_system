from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, AdminRegisterForm


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')   # Redirect to dashboard if logged in
    else:
        return redirect('login')       # Otherwise redirect to login


def register_user_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = False
            user.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register_user.html', {'form': form})

def register_admin_view(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = True
            user.is_staff = True
            user.save()
            return redirect('login')
    else:
        form = AdminRegisterForm()
    return render(request, 'users/register_admin.html', {'form': form})

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')
    return render(request, 'users/login.html', {'form': form})

@login_required
def dashboard_view(request):
    if request.user.is_admin:
        return render(request, 'users/admin_dashboard.html')
    return render(request, 'users/user_dashboard.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
