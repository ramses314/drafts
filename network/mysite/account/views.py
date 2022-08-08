from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.http import require_POST

from actions.models import Action
from actions.utils import create_action
from images.models import Image
from .forms import *

from PIL import Image as IImage


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['name'], password=cd['password'])
#             if user is not None:
#                 login(request, user)
#                 return HttpResponse('Вход выполнен')
#             else:
#                 return HttpResponse('Проверте верность веденного логина')
#         else:
#             return HttpResponse('Невено введены данные')
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form':form})
from .models import Contact


@login_required
def home(request):

    my_acc = request.user.profile


    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)


    lenta = Image.objects.filter(user_id__in=following_ids).exclude(user=request.user)

    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions[:10]

    # actions = actions.select_related('user', 'user__profil').prefetch_related('target')[:10]

    posts = Image.objects.filter(user=request.user)

    return render(request, 'account/home.html', {'someshit': 'homepc', 'action' : actions, 'posts' : posts,
                                                 'mydata' : my_acc,
                                                 'lenta' : lenta})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.photo = IImage.open('account/static/account/img/zero_photo.jpg')

            new_user.save()
            Profile.objects.create(user=new_user)

            create_action(new_user, 'создал аккаунт')
            return render(request, 'account/register_done.html', {'user_form' : user_form})
    else:
        user_form = UserRegistrationForm()

    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        try:
            print(123)
            profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        except:
            print(321)
            Profile.objects.create(user=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Профиль успешно обновлен')
        else:
            messages.error(request, 'Ошибка во вводе информации')

    else:
        user_form = UserEditForm(instance=request.user)

        try:
            profile_form = ProfileEditForm(instance=request.user.profile)
        except:
            Profile.objects.create(user=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)


    return render(request, 'account/edit.html', {'user_form':user_form, 'profile_form':profile_form})



@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html', {'section' : 'people', 'users' : users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html', {'section': 'people', 'user':user})

@login_required
def user_detail2(request, username, lol=None):
    user1 = get_object_or_404(User, username=username, is_active=True)
    print(11, lol)
    print(type(lol))
    if lol != '0':
        user = User.objects.get(username=username)
        Contact.objects.get_or_create(user_from=request.user, user_to=user)
    else:
        print(23)
        user = User.objects.get(username=username)
        Contact.objects.filter(user_from=request.user, user_to=user)

    return render(request, 'account/user/detail.html', {'section': 'people', 'user':user1})



@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    print(111)
    if user_id and action:
        print(222)
        try:
            print(333)
            user = User.objects.get(id=user_id)
            if action == 'follow':
                print(444)
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
            else:
                print(555)
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status' : 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status' : 'ok'})
    return JsonResponse({'status' : 'ok'})