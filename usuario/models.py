# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import FieldError

class Usuario(models.Model):
  """ Clase que extiende funcionalidades de la clase User.

  Este modelo pretende agregar funcionalidades al usuario que viene facilitado
  por django. Este archivo sobreescribe el método __getattr__ de la clase User
  de forma tal que se pueda llamar a los atributos del modelo de esta clase, o
  sus subclases, desde una instancia de User (en caso que hubiere), recordando
  siempre que la relación entre esta clase y la User proporcionada por django es
  uno a uno.

  @type nombre: string
  @type paterno: string
  @type materno: string
  @type foto: Image
  @type user: User

  @ivar nombre: nombre del usuario
  @ivar paterno: apellido paterno del usuario
  @ivar materno: apellido materno del usuario
  @ivar foto: foto del usuario
  @ivar user: modelo User al cual está relacionado
  """

  nombre = models.CharField(max_length=50, null=True)
  paterno = models.CharField(max_length=50, null=True)
  materno = models.CharField(max_length=50, null=True)
  foto = models.ImageField(upload_to="usuarios/", default="usuarios/Anonimo.png")

  user = models.OneToOneField(User)

  def nombre_completo(self):
    return self.nombre+" "+self.paterno+" "+self.materno

  def __init__(self, *args, **kwargs):
    dict = {}
    for key in ['username', 'password', 'first_name', 'last_name', 'email']:
      dict[key] = kwargs.pop(key, None)

    super().__init__(*args, **kwargs)

    for key, value in dict.items():
      if value is not None:
        setattr(self, key, value)

  def save(self, *args, **kwargs):
    """ Se sobreescribe el método salvar para poder gestionar la creación de un
    User en caso que no se haya creado y enlazado uno antes.
    """
    if not hasattr(self, 'user') or self.user is None:
      if hasattr(self, 'password') and hasattr(self, 'username'):
        if not hasattr(self, 'first_name'):
          self.first_name = ""
        if not hasattr(self, 'last_name'):
          self.last_name = ""
        if not hasattr(self, 'email'):
          self.email = ""

        self.user = User.objects.create(
          username=self.username,
          first_name=self.first_name,
          last_name=self.last_name,
          email=self.email,
          password=self.password
        )
      else:
        raise FieldError("Debe ingresar los campos password y username si desea automatizar la creación de un User.")
    else:
      ''' Para que la siguiente comparación tenga sentido la clase Usuario NO
      debe ser abstracta (para django). '''
      if self.user.usuario.pk != self.pk:
        raise FieldError("Debe ingresar User que no tenga relación con ningún Usuario existente.")

    super().save(*args, **kwargs)

def _get_instance(user):
  inst = None
  f = Usuario.objects.filter(user=user)
  if f.count() == 1: # siempre debiese ser 1 ó 0.
    inst = f[0]
    for sub_u in Usuario.__subclasses__():
      if hasattr(inst, sub_u.__name__.lower()):
        inst = getattr(inst, sub_u.__name__.lower())
        break
  return inst

def _new__getattr__(self, name):
  # recolectar los nombres de atributos y métodos válidos
  names = Usuario._meta.get_all_field_names() # atributos
  names += [n for n in Usuario.__dict__.keys() if not n.startswith('_')] # metodos
  for sub_u in Usuario.__subclasses__():
    names += sub_u._meta.get_all_field_names() # atributos
    names += [n for n in sub_u.__dict__.keys() if not n.startswith('_')] # metodos

  if name in names:
    i = _get_instance(self)
    if i != None:
      return getattr(i, name)
  raise AttributeError

setattr(User, '__getattr__', _new__getattr__)

#class NuevoUsuario(Usuario):
#  nombre2 = models.CharField(max_length=50, null=True)
#  def nombre_completo2(self):
#    return self.nombre+" "+self.nombre2+" "+self.paterno+" "+self.materno
