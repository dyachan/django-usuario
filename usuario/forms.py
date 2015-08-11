# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth.hashers import check_password

from usuario.models import Usuario
#from usuario.models import NuevoUsuario

class EditarUsuarioForm(forms.ModelForm):
  """ Formulario para el ingreso y edicion de User

  Este formulario pretende controlar el ingreso y edición de los usuarios que
  ingresan al sistema permitiendo la validación de contraseña y revisar la
  existencia de un nombre de usuario (username) antes de crear o modificar.

  @type username: Char
  @type password_antigua: Char
  @type password: Char
  @type password_repetir: Char
  @type email: Char
  @type nombre: Char
  @type paterno: Char
  @type materno: Char

  @ivar username: nick del usuario
  @ivar password_antigua: contraseña anterior en caso que se esté editando al
   usuario
  @ivar password: contraseña del usuario
  @ivar password_repetir: repetir la contraseña anterior
  @ivar email: correo electrónico del usuario
  @ivar nombre: nombre del usuario
  @ivar paterno: apellido paterno del usuario
  @ivar materno: apellido materno del usuario
  """

  class Meta:
    model = Usuario
    exclude = ['user']

  username = forms.CharField()
  password_antigua = forms.CharField(widget=forms.HiddenInput, required=False)
  password = forms.CharField(widget=forms.PasswordInput)
  password_repetir = forms.CharField(widget=forms.PasswordInput)
  email = forms.CharField(required=False)

  nombre = forms.CharField(required=False)
  paterno = forms.CharField(required=False)
  materno = forms.CharField(required=False)

  def clean(self):
    """ Se agrega la verificación que las contraseñas ingresadas sean iguales
    """

    cleaned_data = super().clean()
    psw = cleaned_data.get("password")
    pswr = cleaned_data.get("password_repetir")

    if psw != pswr:
      self.add_error('password', ValidationError(_('Las claves ingresadas no son iguales'), code='invalid'))

  def clean_password_antigua(self):
    """ Se agrega la verificación que la contraseña anterior ingresada sea la
     contraseña real del usuario
    """

    data = self.cleaned_data['password_antigua']
    if self.instance.pk is not None and not check_password(data, self.instance.user.password):
      raise forms.ValidationError(_('Clave anterior ingresada incorrecta'), code='invalid')
    return data

  def clean_username(self):
    """ Se agrega la verificación que el nock de usuario ingresado esté
     disponible
    """

    data = self.cleaned_data['username']
    if User.objects.filter(username=data).exists():
      if not (self.instance.pk is not None and self.instance.user.username == data):
        raise forms.ValidationError(_('Usuario "%(username)s" ocupado'), code='invalid', params={'username': data})
    return data

  def __init__(self, *args, **kwargs):
    """ Se llenan los campos de User si se está editando al usuario y se hace necesario el campo de contraseña anterior
    """

    super().__init__(*args, **kwargs)
    if self.instance.pk is not None:
      # caso se está editando al usuario
      self.fields['username'].initial = kwargs['instance'].user.username
      self.fields['email'].initial = kwargs['instance'].user.email

      self.fields['password_antigua'].required = True
      self.fields['password_antigua'].widget = forms.PasswordInput()

  def save(self, force_insert=False, force_update=False, commit=True):
    """ Se sobreescribe el método save para crear o modificar al User en caso
     que el parámetro commit sea True.
    """

    usuario = super().save(commit=False)
    if commit:
      user = None
      if self.instance.pk is not None:
        user = usuario.user
      else:
        user = User()
      user.username = self.cleaned_data['username']
      user.set_password(self.cleaned_data['password'])
      user.email = self.cleaned_data['email']
      user.save()
      usuario.user = user
      usuario.save()
    return usuario

#class EditarNuevoUsuarioForm(EditarUsuarioForm):
#  class Meta:
#    model = NuevoUsuario
#    exclude = ['nombre2', 'user']
