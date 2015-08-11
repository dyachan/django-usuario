# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError

from usuario.models import Usuario
#from usuario.models import NuevoUsuario

from usuario.forms import EditarUsuarioForm
#from usuario.forms import EditarNuevoUsuarioForm

class test_form(TestCase):

  def setUp(self):
    super().setUp()

#  def test_crear_nuevousuario_basico(self):
#    f = EditarNuevoUsuarioForm({'username': "a", 'password': "b", 'password_repetir': "b"})
#    self.assertTrue(f.is_valid())
#    f.save()
#    self.assertEqual(NuevoUsuario.objects.all().count(), 1)
#    self.assertEqual(User.objects.all().count(), 1)

  def test_ingresar_clave_anterior_correctamente(self):
    u = Usuario.objects.create(username="a", password="b")
    f = EditarUsuarioForm({'username': "a", 'password_antigua': "b", 'password': "c", 'password_repetir': "c"}, instance=u)
    self.assertTrue(f.is_valid())

  def test_clave_anterior_requerida_si_es_instancia(self):
    u = Usuario.objects.create(username="a", password="b", email="c")
    f = EditarUsuarioForm(instance=u)
    self.assertTrue(f['password_antigua'].field.required)

  def test_mostrar_clave_anterior_si_es_instancia(self):
    u = Usuario.objects.create(username="a", password="b", email="c")
    f = EditarUsuarioForm(instance=u)
    self.assertTrue(f['password_antigua'] in f.visible_fields())

  def test_no_repetir_usuario(self):
    u = Usuario.objects.create(username="a", password="b", email="c")
    f = EditarUsuarioForm({'username': "a", 'password': "b", 'password_repetir': "b"})
    self.assertFalse(f.is_valid())

  def test_reescribir_clave_correctamente(self):
    f = EditarUsuarioForm({'username': "a", 'password': "b", 'password_repetir': "c"})
    self.assertFalse(f.is_valid())

  def test_autorellenar_campos_user_si_hay_instancia(self):
    u = Usuario.objects.create(username="a", password="b", email="c")
    f = EditarUsuarioForm(instance=u)
    self.assertEqual(f['username'].value(), u.user.username)
    self.assertEqual(f['email'].value(), u.user.email)

  def test_crear_usuario_basico(self):
    f = EditarUsuarioForm({'username': "a", 'password': "b", 'password_repetir': "b"})
    self.assertTrue(f.is_valid())
    f.save()
    self.assertEqual(Usuario.objects.all().count(), 1)
    self.assertEqual(User.objects.all().count(), 1)

class test_usuario(TestCase):

  def setUp(self):
    super().setUp()

#  def test_acceder_a_campos_nuevo_usuario(self):
#    u = NuevoUsuario.objects.create(
#      username="qqq",
#      password="www",
#      nombre="eee",
#      paterno="rrr",
#      materno="ttt",
#      nombre2="uuu")
#    self.assertEqual(u.user.nombre2, "uuu")

#  def test_crear_nuevo_usuario(self):
#    u = NuevoUsuario.objects.create(
#      username="qqq",
#      password="www",
#      nombre="eee",
#      paterno="rrr",
#      materno="ttt",
#      nombre2="uuu")
#    self.assertEqual(User.objects.all().count(), 1)
#    self.assertEqual(Usuario.objects.all().count(), 1)
#    self.assertEqual(NuevoUsuario.objects.all().count(), 1)

#  def test_generar_nombre_completo_de_nuevo_usuario_por_user(self):
#    u = NuevoUsuario.objects.create(
#      username="qqq",
#      password="www",
#      nombre="eee",
#      paterno="rrr",
#      materno="ttt",
#      nombre2="uuu")
#    self.assertEqual(u.user.nombre_completo2(), "eee uuu rrr ttt")

#  def test_modificar_NuevoUsuario_y_modificar_User(self):
#    u = NuevoUsuario.objects.create(
#      username="qqq",
#      password="www",
#      nombre="eee",
#      nombre2="uuu")
#
#    u.user.username = "yyy"
#    u.save()
#
#    self.assertEqual(User.objects.all()[0].username, "yyy")

  def test_al_modificar_Usuario_sin_modificar_User(self):
    u = Usuario.objects.create(
      username="qqq",
      password="www",
      nombre="eee",
      paterno="rrr",
      materno="ttt")

    u.user.username = "yyy"
    u.save(UserSave=False)

    self.assertEqual(User.objects.all()[0].username, "qqq")

  def test_al_modificar_Usuario_y_modificar_User(self):
    u = Usuario.objects.create(
      username="qqq",
      password="www",
      nombre="eee",
      paterno="rrr",
      materno="ttt")

    u.user.username = "yyy"
    u.save()

    self.assertEqual(User.objects.all()[0].username, "yyy")

  def test_error_al_dar_user_con_otro_usuario_asignado(self):
    u = Usuario.objects.create(
      username="qqq",
      password="www",
      nombre="eee",
      paterno="rrr",
      materno="ttt")
    self.assertRaises(IntegrityError, Usuario.objects.create, user=u.user)

  def test_error_al_no_dar_atributos_de_user(self):
    u = Usuario(
      nombre="eee",
      paterno="rrr",
      materno="ttt")

    self.assertRaises(IntegrityError, u.save)

  def test_generar_nombre_completo_por_usuario(self):
    u = Usuario(
      username="qqq",
      password="www",
      nombre="eee",
      paterno="rrr",
      materno="ttt")

    self.assertEqual(u.nombre_completo(), "eee rrr ttt")

  def test_generar_nombre_completo_por_user(self):
    u = Usuario.objects.create(
      username="qqq",
      password="www",
      nombre="eee",
      paterno="rrr",
      materno="ttt")

    self.assertEqual(u.user.nombre_completo(), "eee rrr ttt")

  def test_acceder_a_campos_por_user(self):
    u = Usuario.objects.create(
      username="qqq",
      password="www",
      nombre="eee",
      paterno="rrr",
      materno="ttt")

    self.assertEqual(u.user.nombre, "eee")
    self.assertEqual(u.user.materno, "ttt")
    self.assertEqual(u.user.paterno, "rrr")

  def test_crear_usuario_por_campos_sin_user(self):
    u = Usuario()
    u.username = "qqq"
    u.password = "www"
    u.nombre = "eee"
    u.paterno = "rrr"
    u.materno = "ttt"

    u.save()
    self.assertEqual(User.objects.all().count(), 1)
    self.assertEqual(Usuario.objects.all().count(), 1)

  def test_crear_usuario_por_parametros_sin_user(self):
    u = Usuario(
      username="qqq",
      password="www",
      nombre="eee",
      paterno="rrr",
      materno="ttt")

    u.save()
    self.assertEqual(User.objects.all().count(), 1)
    self.assertEqual(Usuario.objects.all().count(), 1)

  def test_crear_usuario_con_create_sin_user(self):
    u = Usuario.objects.create(
      username="qqq",
      password="www",
      nombre="eee",
      paterno="rrr",
      materno="ttt")

    self.assertEqual(User.objects.all().count(), 1)
    self.assertEqual(Usuario.objects.all().count(), 1)

  def test_crear_usuario_por_campos_con_user(self):
    user = User.objects.create(password="yyy", username="uuu")
    u = Usuario()
    u.username = "qqq"
    u.password = "www"
    u.nombre = "eee"
    u.paterno = "rrr"
    u.materno = "ttt"
    u.user = user

    u.save()
    self.assertEqual(User.objects.all().count(), 1)
    self.assertEqual(Usuario.objects.all().count(), 1)
    self.assertEqual(Usuario.objects.all()[0].user.pk, user.pk)

  def test_crear_usuario_por_parametros_con_user(self):
    user = User.objects.create(password="yyy", username="uuu")
    u = Usuario(
      username="qqq",
      password="www",
      nombre="eee",
      paterno="rrr",
      materno="ttt",
      user=user)

    u.save()
    self.assertEqual(User.objects.all().count(), 1)
    self.assertEqual(Usuario.objects.all().count(), 1)
    self.assertEqual(Usuario.objects.all()[0].user.pk, user.pk)

  def test_crear_usuario_con_create_con_user(self):
    user = User.objects.create(password="yyy", username="uuu")
    u = Usuario.objects.create(
      username="qqq",
      password="www",
      nombre="eee",
      paterno="rrr",
      materno="ttt",
      user=user)

    self.assertEqual(User.objects.all().count(), 1)
    self.assertEqual(Usuario.objects.all().count(), 1)
