from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.

def user_list(request):
    return render(request, 'chatapp/user_list.html')

def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect('list/')
        else:
            print(form.errors)
    return render(request, 'chatapp/login.html', {'form': form})

@login_required(login_url='/log_in/')
def log_out(request):
    logout(request)
    return redirect(reverse('chatapp:log_in'))

def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
        else:
            print(form.errors)
    return render(request, 'chatapp/sign_up.html', {'form': form})

User = get_user_model()

@login_required(login_url='/log_in/')
def user_list(request):
    users = User.objects.select_related('logged_in_user')
    for user in users:
        user.status = 'Online' if hasattr(user, 'logged_in_user') else 'Offline'
    return render(request, 'chatapp/user_list.html', {'users': users})
