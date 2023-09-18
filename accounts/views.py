from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, PasswordChangingForm, \
    ProfileAdminForm
from .models import Profile


# Create your views here.
def loginview(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # print(form)
        if form.is_valid():
            # print(form)
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password'])
            # print(user.username)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index_view')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logoutview(request):
    if request.method == 'POST':
        logout(request)
        return redirect('registration/login.html')

    return render(request, 'registration/logged_out.html', {})


@login_required
def user_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'profile/profile.html', context)


from .models import Profile
def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileAdminForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            context = {
                'new_user':new_user
            }
            return render(request, 'account/register_done.html', context)
        else:
            return HttpResponse('This username is already taken.')
    else:
        user_form = UserRegistrationForm()
        profile = ProfileAdminForm()
        context = {
            'user_form': user_form,
            'profile': profile
        }
        return render(request, 'account/register.html', context)
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/register.html'


@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        else:
            return render(request, 'account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})


class EditUserView(LoginRequiredMixin, View):

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        return render(request, 'account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        if request.method == 'POST':
            user_form = UserEditForm(instance=request.user, data=request.POST)
            profile_form = ProfileEditForm(
                instance=request.user.profile, data=request.POST, files=request.FILES)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('profile')
