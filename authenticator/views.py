from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, ContestantProfileForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.conf import settings

def anonymous_required(function=None, redirect_url=None):

   if not redirect_url:
       redirect_url = settings.LOGIN_REDIRECT_URL

   actual_decorator = user_passes_test(
       lambda u: u.is_anonymous,
       login_url=redirect_url
   )

   if function:
       return actual_decorator(function)
   return actual_decorator

@anonymous_required
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('register-success')
        else:
            context = {'form': form,
                       'validation' : True,}
            return render(request, 'registration/register.html', context=context)
    else:
        context = {'form': RegistrationForm(),
                   'validation' : False,}
        return render(request, 'registration/register.html', context=context)

def register_success_view(request):
    return render(request, 'registration/register_success.html')

@anonymous_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        form = AuthenticationForm(request.POST)

        try:
            user = User.objects.get(username=username)
        except:
            context = {'form': form,
                       'validation' : True,
                       'error': f'Username \"{username}\" not found.',
                       'username_error': True,}
            return render(request, 'registration/login.html', context=context)
            
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request, user)
            
            return redirect('home')
        else:
            context = {'form': form,
                       'validation' : True,
                       'error': "Username and password do not match."}

        return render(request, 'registration/login.html', context=context)
    else:
        context = {'form': AuthenticationForm(),
                   'validation' : False,}
        return render(request, 'registration/login.html', context=context)
    

class LogoutView(TemplateView):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        logout(request)
        return redirect('home')

def CreateContestantProfileView(request):
    user = request.user
    if user is None:
        return redirect('login')
    if request.method == 'POST':
        form = ContestantProfileForm(request.POST, request.FILES)
        if form.is_valid():
            contestant = form.save(commit=False)
            contestant.user = user
            contestant.save()
            return redirect('home')
    else:
        form = ContestantProfileForm()
    return render(request, 'contestant_profile_create.html', {'form': form, 'user': user})

def ContestantProfileView(request, user_id):
    user = get_object_or_404(User, id=user_id)
    contestant = get_object_or_404(Contestant, user=user)
    return render(request, 'contestant_profile_view.html', {'contestant': contestant})