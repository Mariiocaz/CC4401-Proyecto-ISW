from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm

class NewCategoryForm(forms.ModelForm):
  nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingresa un nombre', 'size': 50, 'class': 'form-control'}))
  
  class Meta:
    model = Categoria
    fields = ['nombre']
    
class NewTransactionForm(forms.ModelForm):
  titulo = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingresa un nombre', 'size': 50, 'class': 'form-control'}))
  monto = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': 'Ingresa un nombre', 'size': 50, 'class': 'form-control'}))
  fecha_creacion = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
  categoria = forms.ModelChoiceField(queryset=None)
  
  class Meta:
    model = Transaccion
    fields = ['titulo', 'monto', 'fecha_creacion', 'categoria']
    
  
  def __init__(self, *args, **kwargs):
    user = kwargs.pop('user', None)
    super().__init__(*args, **kwargs)
    self.fields['categoria'].queryset = self.get_user_categorias(user)

  def get_user_categorias(self, user):
    if user:
      return user.categoria.all()
    return Categoria.objects.none()
  
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

  