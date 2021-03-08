""" 
Let's start by building a form to submit new images.
"""
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
from .models import Image

class ImageCreateForm(forms.ModelForm):
    """ 
    This form is a ModelFOrm form built from the image model
    including only the title, url and description fields.
    Users will not enter the image url directly in the form.
    instead you will provide them with JS tool to choose an image
    from an external site, and your form will receive its url as a parameter.
    You override the default widget of the url field to HiddenInput.
    This widget is rendered as html input element whit a type "hidden" attribute.
    You use this widget because you don't want this field to be visible to users.
    """
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        """
        You define a clean_url method to clean the url field.
        You get the value of the url by accessing the cleaned_data
        dictionary of the form instance
        You split the URL to get the file extension and check
        whether it is one of the valid extensions. If the extension
        is invalid, you raise ValidationError and the form instance
        will not be validated. Here you are performing a very simple
        validation. You could use more advanced methods to check
        whether the given URL provides a valid image file.
        """
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('La URL recibida no es compatible con la'\
                                        ' extension de imagenes')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        # download image from the given URL
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)

        if commit:
            image.save()
        return image
