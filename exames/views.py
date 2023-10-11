from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TipoExames, PedidosExames, SolicitacaoExame, AcessoMedico
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants


@login_required
def solicitar_exames(request):
    tipos_exames = TipoExames.objects.all()
    if request.method == "GET":

        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames})
    
    elif request.method == 'POST':
        #como lá temos mais de um valor, o get só pega um ID de cada vez, então devemos usar o getlist
        exames_id = request.POST.getlist ('exames')
        solicitar_exames = TipoExames.objects.filter(id__in=exames_id)
        #aqui fazemos um filtro mais complexo onde faz uma busca dos dados do Tipo_exames e procura se dentro da lista de exames_id existe algo igual 
        
        preco_total =0
        for i in solicitar_exames:
            if i.disponivel == True:
                preco_total +=i.preco

            data_atual = datetime
            context = {
                'tipos_exames': tipos_exames,
                'solicitar_exames': solicitar_exames,
                'preco_total': preco_total,
                'data': data_atual

            }
        
    
        return render(request, 'solicitar_exames.html', context)

@login_required
def fechar_pedido(request):
    exames_id = request.POST.getlist('exames')
    solicitacao_exames = TipoExames.objects.filter(id__in=exames_id)

    pedido_exame = PedidosExames(
        usuario = request.user,
        data=datetime.now()
    )
    pedido_exame.save()

    for exame in solicitacao_exames:
        solicitacao_exames_temp = SolicitacaoExame(
            usuario=request.user,
            exame=exame,
            status="E"
        )
        solicitacao_exames_temp.save()
        pedido_exame.exames.add(solicitacao_exames_temp)
        #Aqui eu faço o relacionamento dos exames solicitados para o manyTomany exames da classe PedidoExames
        #Vinculando cada solicitação para o Pedido de Exame
    pedido_exame.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido de exame realizado com sucesso.')
    return redirect('gerenciar_pedidos')

@login_required
def gerenciar_pedidos(request):
    pedidos_exames = PedidosExames.objects.filter(usuario=request.user)
    #aqui buscamos todos os pedidos no BD que é do usuário logado
    context={
        'pedidos_exames': pedidos_exames
    }
    return render(request, 'gerenciar_pedidos.html', context)

@login_required
def cancelar_pedido(request, pedido_id):
    pedido = PedidosExames.objects.get(id=pedido_id)
    
    if not pedido.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Esse pedido não é seu, você não pode cancelar.')
        return redirect('gerenciar_pedidos')

    pedido.agendado = False
    pedido.save()
    
    messages.add_message(request, constants.SUCCESS, 'Pedido cancelado com sucesso.')

    return redirect('gerenciar_pedidos')

@login_required
def gerenciar_exames(request):
    exames = SolicitacaoExame.objects.filter(usuario=request.user)

    return render(request, 'gerenciar_exames.html', {'exames': exames})

@login_required
def permitir_abrir_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)

    if not exame.requer_senha:
        if exame.resultado.url != '' and exame.status == 'F':
            return redirect(exame.resultado.url)

    return redirect(f'/exames/solicitar_senha_exame/{exame.id}')
    
@login_required
def solicitar_senha_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    if request.method == 'GET':
        return render(request, 'solicitar_senha_exame.html', {'exame': exame})
    elif request.method == 'POST':
        senha = request.POST.get("senha")
        
        if exame.senha == senha:
            if exame.resultado.url != '' and exame.status == 'F':
                return redirect(exame.resultado.url)
        else:
            messages.add_message(request, constants.ERROR, 'Senha inválida.')
            return redirect(f'/exames/solicitar_senha_exame/{exame.id}')

@login_required
def gerar_acesso_medico(request):
    if request.method == 'GET':
        acesso_medico = AcessoMedico.objects.filter(usuario=request.user)
        return render(request, 'gerar_acesso_medico.html', {'acesso_medico':acesso_medico})
    
    elif request.method == 'POST':
        identificacao = request.POST.get('identificacao')
        tempo_de_acesso = request.POST.get('tempo_de_acesso')
        data_exame_inicial = request.POST.get("data_exame_inicial")
        data_exame_final = request.POST.get("data_exame_final")

        acesso_medico = AcessoMedico(
            usuario = request.user,
            identificacao = identificacao,
            tempo_de_acesso = tempo_de_acesso,
            data_exames_iniciais = data_exame_inicial,
            data_exames_finais = data_exame_final,
            criado_em = datetime.now()
        )

        acesso_medico.save()

        messages.add_message(request, constants.SUCCESS, 'Acesso gerado com sucesso')
        return redirect('gerar_acesso_medico')
    
def acesso_medico(request, token):
    acesso = AcessoMedico.objects.get(token=token)
    if acesso.status == "Expirado":
        messages.add_message(request, constants.ERROR, 'Esse token já expirou, solicite outro.')
        return redirect('login')
    else:
        pedidos = PedidosExames.objects.filter(usuario=acesso.usuario).filter(data__gte=acesso.data_exames_iniciais).filter(data__lte=acesso.data_exames_finais)
        #gte significa maior ou igual e lte significa menor ou igual
        
        return render(request, 'acesso_medico.html', {'pedidos': pedidos})
