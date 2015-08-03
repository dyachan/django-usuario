# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models, IntegrityError

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

  def save(self, UserSave=True, *args, **kwargs):
    """ Se sobreescribe el método salvar para poder gestionar la creación de un
    User en caso que no se haya creado y enlazado uno antes.
    Se puede elegir si se desea guardar los cambios efectuados en user.
    """

    if hasattr(self, 'user') and self.user is not None:
      # caso que se le asigna un usuario determinado
      if hasattr(self.user, 'usuario') and self.user.usuario is not None:
        # caso que se le haya asignado un usuario
        if self.user.usuario.pk != self.pk:
          # caso el usuario asignado ya tiene a otro
          raise IntegrityError("Debe ingresar User que no tenga relación con ningún Usuario existente.")
        else:
          # en este caso se debe revisar si hay que modificar User
          pass
    else:
      # caso que No tenga un usuario asignado de antemano
      if not hasattr(self, 'password') or not hasattr(self, 'username'):
        # caso que no tenga los atributos password y/o username
        raise IntegrityError("Debe ingresar los campos password y username si desea automatizar la creación de un User.")
      else:
        if not hasattr(self, 'first_name'):
          self.first_name = ""
        if not hasattr(self, 'last_name'):
          self.last_name = ""
        if not hasattr(self, 'email'):
          self.email = ""

        user = User(
          username=self.username,
          first_name=self.first_name,
          last_name=self.last_name,
          email=self.email
        )
        # almacenar password de forma segura
        user.set_password(self.password)
        user.save()
        self.user = user

        # eliminar los atributos que no se debiesen estar en la instancia
        for name in ['username', 'password', 'first_name', 'last_name', 'email']:
          delattr(self, name)

    # se guarda  Usuario y User en caso que se haya modificado
    super().save(*args, **kwargs)
    if UserSave:
      self.user.save()

def _get_instance(user):
  """ función que busca la instancia de la clase hija más baja de Usuario y que
  esté enlazada con el usuario dado por parámetro.
  """

  inst = None
  f = Usuario.objects.filter(user=user)
  if f.exists():
    inst = f[0]
    for sub_u in Usuario.__subclasses__():
      if hasattr(inst, sub_u.__name__.lower()):
        inst = getattr(inst, sub_u.__name__.lower())
        break
  return inst

def _new__getattr__(self, name):
  """ función que sobreescribirá el método del mismo nombre de la clase User
  """

  # recolectar los nombres de atributos y métodos válidos
  names = Usuario._meta.get_all_field_names() # atributos
  names += [n for n in Usuario.__dict__.keys() if not n.startswith('_')] # metodos

  # recolectar los nombres de los atributos y métodos válidos de las subclases
  for sub_u in Usuario.__subclasses__():
    names += sub_u._meta.get_all_field_names() # atributos
    names += [n for n in sub_u.__dict__.keys() if not n.startswith('_')] # metodos

  if name in names:
    i = _get_instance(self)
    if i != None:
      return getattr(i, name)
  raise AttributeError("'User' object has no attribute '%s'" % name)

setattr(User, '__getattr__', _new__getattr__)

#class NuevoUsuario(Usuario):
#  nombre2 = models.CharField(max_length=50, null=True)
#  def nombre_completo2(self):
#    return self.nombre+" "+self.nombre2+" "+self.paterno+" "+self.materno
