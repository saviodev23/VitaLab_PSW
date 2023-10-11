from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        usuario = request.POST.get('username')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não são iguais.')
            return redirect('cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.WARNING, 'Sua senha deve ter 6 ou mais digitos.')
            return redirect('cadastro') 
        
        try:
            #validar se já existe um usuario semelhante ao banco de dados
            usuario_existente = User.objects.filter(username=usuario)
            if usuario_existente.exists():
                messages.add_message(request, constants.ERROR, 'Usuário já existente no sistema.')
            
            user = User.objects.create(
                first_name = primeiro_nome,
                last_name = ultimo_nome,
                username = usuario,
                email = email,
                password=make_password(senha)
            )
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema, contate um administrador..')
            return redirect('cadastro')
    

        return redirect('cadastro')
    
   
def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        usuario = request.POST.get('username')
        senha = request.POST.get('senha')

        #verifica se há o usuario no banco de dados
        user = authenticate(username=usuario, password=senha)

        if user:
            login(request, user)
			# Acontecerá um erro ao redirecionar por enquanto, resolveremos nos próximos passos
            return redirect('teste')
        else:
            messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
            return redirect('login')
        

def teste(request):
    return HttpResponse('Logado no sistema!')