from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from AppBlog.models import Avatar

class FormularioPosteo(forms.Form):

    autor = forms.CharField(max_length = 40)
    email = forms.EmailField()
    titulo = forms.CharField(max_length = 40)
    cuerpo = forms.CharField(widget=forms.Textarea)

class FormularioBusqueda(forms.Form):

    titulo = forms.CharField(max_length=40)

class FormularioRegistroUsuario(UserCreationForm):

    password1 = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Confirme su contraseña', widget = forms.PasswordInput)

    class Meta:
        
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {'username': None, 'password1': None, 'password2': None}

class AvatarFormulario(forms.ModelForm):

    class Meta:

        model = Avatar
        fields = ['user', 'imagen']