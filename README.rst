=======
Usuario
=======

Usuario es una extensión al modelo User de Django que permite el usar una instancia de User (manejo de permisos, pertenencia a grupos) y además poder usar desde esa instancia campos agregados por el usuario. Por defecto ya vienen agregados 4 campos: nombre, apellido paterno, apellido materno y foto (una simple imagen).

Quick start
-----------

1. Agregue "usuario" a su INSTALLED_APPS en el archivo setting de la siquiente forma::

    INSTALLED_APPS = (
        ...
        'usuario',
        ...
    )

2. Al interior de la carpeta /MEDIA/usuarios/ (crearla si no existe) agregar una imagen llamada "Anonimo.png" que servirá de imagen por defecto para un usuario

3. Ejecutar `python manage.py migrate` para crear el modelo Usuario.

OPCIONAL
--------

1. Si quiere extender más la clase Usuario simplemente debe crear otro modelo que se herede de esa clase tal como se muestra a continuación::

    class NuevoUsuario(Usuario):
        campo_nuevo = models.CharField(max_length=50, null=True)
        def get_campo_nuevo(self):
            return self.campo_nuevo

2. Ejecutar `python manage.py migrate` para crear el modelo NuevoUsuario.

3. Podrá crear nuevas instancias de su modelo::

    >>> u = NuevoUsuario.objects.create(username="a", password="b", nombre="c", campo_nuevo="d")

4. Podrá acceder a los diferentes campos de la siguiente forma::

    >>> u = User.objects.get(username="a")
    >>> u.nombre
    <<< 'c'
    >>> u.nuevo_campo
    <<< 'd'
    >>> u.get_nuevo_campo()
    <<< 'd'
