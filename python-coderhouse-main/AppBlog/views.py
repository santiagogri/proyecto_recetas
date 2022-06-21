from django.shortcuts import redirect, render
from AppBlog.forms import FormularioPosteo, FormularioRegistroUsuario, AvatarFormulario
from AppBlog.models import Avatar, Posteo, Comentario
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

# Vista Inicio
def inicio(request):

    id = 1
    listadoPosteos = Posteo.objects.all()
    diccionario = {'id': id, 'listadoPosteos': listadoPosteos}
    return render(request,'AppBlog/inicio.html', diccionario)

# Vista Sobre Nosotros
def sobreNostros(request):

    id = 2
    diccionario = {'id': id}
    return render(request,'AppBlog/sobreNosotros.html', diccionario)

# Vista para hacer un posteo
@login_required
def hacerPosteo(request):

    if request.method == 'POST':

        miPosteo = FormularioPosteo(request.POST)

        print(miPosteo)

        if miPosteo.is_valid():

            contenido = miPosteo.cleaned_data

            posteo = Posteo(autor = contenido['autor'], email = contenido['email'], titulo = contenido['titulo'], cuerpo = contenido['cuerpo'])

            posteo.save()

            listadoPosteos = Posteo.objects.all()
            return render(request,'AppBlog/inicio.html', {'mensaje': f'¡Posteo creado!', 'listadoPosteos': listadoPosteos})
    else:

        miPosteo = FormularioPosteo()

    id = 3
    diccionario = {'id': id, 'miPosteo': miPosteo}
    return render(request,'AppBlog/hacerPosteo.html', diccionario)

# Vista para buscar un posteo
def buscar(request):

    data = request.GET.get('titulo', '')

    error = ''

    if data:

        try:
            posteo = Posteo.objects.get(titulo = data)
            return render(request, 'AppBlog/buscar.html', {'posteo': posteo, 'titulo': data})

        except Exception as exc:
            print(exc)
            error = '¡No se encontraron posteos con el título indicado!'

    id = 4
    diccionario = {'id': id, 'error': error}
    return render(request,'AppBlog/buscar.html', diccionario)

# Vista para ver en detalle un posteo
def abrirPosteo(request, titulo):

        leerPosteo = Posteo.objects.get(titulo = titulo)

        try:
            comentario = Comentario.objects.get(titulo = titulo)

            return render(request, 'AppBlog/posteo.html', {'posteo': leerPosteo, 'comentario': comentario})
        
        except:

            return render(request, 'AppBlog/posteo.html', {'posteo': leerPosteo})

# Vista para iniciar sesión
def iniciarSesion(request):

    if request.method == 'POST':

        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            
            usuario = form.cleaned_data.get('username')
            contra = form.cleaned_data.get('password')

            user = authenticate(username = usuario, password = contra)

            if user is not None:

                login(request, user)

                listadoPosteos = Posteo.objects.all()

                return render(request, 'AppBlog/inicio.html', {'mensaje': f'¡Bienvenido {user}!','listadoPosteos': listadoPosteos}) 

            else:

                return render(request, 'AppBlog/login.html', {'errors': ['El usuario no existe.']})

        else:
            
            form = AuthenticationForm()
            return render(request, 'AppBlog/login.html', {'form': form, 'errors': ['¡Usuario y/o contraseña incorrectos!']})
    
    else:
        id = 5
        form = AuthenticationForm()
        diccionario = {'id': id, 'form': form}
        return render(request,'AppBlog/login.html', diccionario)

#Vista para registrarse
def registro(request):
    
    if request.method == 'POST':

        registerForm = FormularioRegistroUsuario(request.POST)

        if registerForm.is_valid():

            user = registerForm.cleaned_data['username']
            
            registerForm.save()

            listadoPosteos = Posteo.objects.all()

            return render(request, 'AppBlog/inicio.html', {'mensaje': f'¡Usuario {user} creado!','listadoPosteos': listadoPosteos})

    else:

        registerForm = FormularioRegistroUsuario()
        
    id = 6
    diccionario = {'id': id, 'registerForm': registerForm}
    return render(request, 'AppBlog/register.html', diccionario)

#Vista para ver lista de posteos
@login_required
def listarPosteos(request):

    id = 7
    listadoPosteos = Posteo.objects.all()
    diccionario = {'id': id, 'listadoPosteos': listadoPosteos}
    return render(request,'AppBlog/listaPosteos.html', diccionario)

#Vista para borrar un posteo
@login_required
def borrarPosteos(request, posteo_titulo):
    
    posteo = Posteo.objects.get(titulo = posteo_titulo)

    posteo.delete()

    id = 7
    listadoPosteos = Posteo.objects.all()
    diccionario = {'id': id, 'listadoPosteos': listadoPosteos}
    return render(request,'AppBlog/listaPosteos.html', diccionario)

#Vista para editar un posteo
@login_required
def editarPosteos(request, posteo_titulo):
    
    posteo = Posteo.objects.get(titulo = posteo_titulo)

    if request.method == 'POST':

        editForm = FormularioPosteo(request.POST)

        if editForm.is_valid():

            contenido = editForm.cleaned_data

            posteo.autor = contenido['autor']
            posteo.email = contenido['email']
            posteo.titulo = contenido['titulo']
            posteo.cuerpo = contenido['cuerpo']
            posteo.save()

            listadoPosteos = Posteo.objects.all()
            return render(request, 'AppBlog/inicio.html', {'mensaje': f'¡Posteo Editado!', 'listadoPosteos': listadoPosteos})
    else:

        editForm = FormularioPosteo(initial = {'autor': posteo.autor, 'email': posteo.email, 'titulo': posteo.titulo, 'cuerpo':  posteo.cuerpo})

    id = 8
    diccionario = {'id': id, 'editForm': editForm, 'posteo_titulo': posteo_titulo}
    return render(request,'AppBlog/editarPosteo.html', diccionario)

#Vista para editar un usuario
@login_required
def editarUsuario(request):
    
    usuario = request.user

    if request.method == 'POST':

        editForm = FormularioRegistroUsuario(request.POST)

        if editForm.is_valid():

            contenido = editForm.cleaned_data

            usuario.username = contenido['username']
            usuario.password1 = contenido['password1']
            usuario.password2 = contenido['password2']
            usuario.save()

            listadoPosteos = Posteo.objects.all()
            return render(request, 'AppBlog/inicio.html', {'mensaje': f'¡Usuario {usuario.username} Editado!', 'listadoPosteos': listadoPosteos})
    else:

        editForm = FormularioRegistroUsuario(initial = {'username': usuario.username})

    id = 9
    diccionario = {'id': id, 'editForm': editForm, 'usuario': usuario.username}
    return render(request,'AppBlog/editarUsuario.html', diccionario)

#Vista para subir avatar
@login_required
def agregarAvatar(request):

    if request.method == 'POST':

        form = AvatarFormulario(request.POST, request.FILES)

        if form.is_valid():

            contenido = form.cleaned_data

            avatar = Avatar(user = contenido['user'], imagen = contenido['imagen'])

            avatar.save()

            listadoPosteos = Posteo.objects.all()
            return render(request, 'AppBlog/inicio.html', {'mensaje': f'¡Avatar Agregado!', 'listadoPosteos': listadoPosteos})

    else:

        form = AvatarFormulario()
    
    id = 10
    diccionario = {'id': id, 'form': form}
    return render(request, 'AppBlog/agregarAvatar.html', diccionario)
