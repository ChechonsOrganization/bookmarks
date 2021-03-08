from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    """ 
    * Este formulario sera utilizado para autenticar usuarios através de la BBDD.
    * El widget de password es para convertir el textarea en tipo password
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Las contraseñas no coinciden')
            return cd['password2']

class UserEditForm(forms.ModelForm):
    """ 
        This will allow to users to edit their first name, last name
        and email with are attributes of the built in django user model
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    """ 
        This will allow users to edit the profile data that you save
        in the custom Profile model. Users will be able to edit their
        date of birth and upload a picture for their profile.
    """
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')