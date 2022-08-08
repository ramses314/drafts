from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from actions.utils import create_action
from .forms import *
# from ..op.utils import create_action

import redis
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()

            create_action(request.user, 'посст', new_item)
            messages.success(request, 'Запись создана')

            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/create.html', {'section' : 'images', 'form' : form})


def post_detail(request, id , slug):
    image = get_object_or_404(Image, id=id, slug=slug)

    total_views = r.incr('image:{}:views'.format(image.id))

    return render(request, 'images/detail.html', {'image' : image,
                                                  'total_views' : total_views})
