from urllib import request

from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'description')
        widgets = {'url' : forms.HiddenInput,
                   'title' : forms.TextInput(attrs={'placeholder' : 'Название'}),
                   }

    # def clean_url(self):
    #     url = self.cleaned_data['url']
    #     valid = ['jpg', 'jpeg']
    #     ext = url.split('.', 1)[1].lower()
    #     if ext not in valid:
    #         raise forms.ValidationError('не товой формат дорогой!')
    #     return url
    #
    # def save(self,  force_insert=False, force_update=False, commit=True):
    #     image = super(ImageCreateForm, self).save(commit=False)
    #     image_url = self.cleaned_data['url']
    #     image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())
    #
    #     response = request.urlopen(image_url)
    #     image.image.save(image_name, ContentFile(response.read()), save=False)
    #     if commit:
    #         image.save()
    #     return image
