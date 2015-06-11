# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User

from usuario.models import Usuario
#from usuario.models import NuevoUsuario

class test_usuario(TestCase):

  def setUp(self):
    super(test_usuario, self).setUp()

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
