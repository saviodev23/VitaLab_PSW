from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe #serve para converter o texto HTML para pagina html
from secrets import token_urlsafe
from django.utils import timezone
from datetime import timedelta

class TipoExames(models.Model):
    TIPO_EXAME = (
        ('I', 'Exame de imagem'),
        ('S', 'Exame de sangue')
    )
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50, choices=TIPO_EXAME)
    preco = models.FloatField()
    disponivel = models.BooleanField(default=True)
    horario_inicial = models.IntegerField()
    horario_final = models.IntegerField()

    def __str__(self):
        return self.nome


class SolicitacaoExame(models.Model):
    choice_status = (
        ('E', 'Em análise'),
        ('F', 'Finalizado')
    )
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exame = models.ForeignKey(TipoExames, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=choice_status)
    resultado = models.FileField(upload_to="resultados", null=True, blank=True)
    requer_senha = models.BooleanField(default=False)
    senha = models.CharField(max_length=6, null=True, blank=True)
    
    def badge_templates(self):
        if self.status == 'E':
            classes = 'bg-warning'
            texto = 'Em análise'
        elif self.status == 'F':
            classes = 'bg-sucess'
            texto = 'Finalizado'
        return mark_safe('<span class="badge {classes}">{texto}</span>')

    def __str__(self):
        return f'{self.usuario} | {self.exame.nome}'
    
class PedidosExames(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exames = models.ManyToManyField(SolicitacaoExame)
    agendado = models.BooleanField(default=True)
    data = models.DateField()

    def __str__(self):
        return f'{self.usuario} | {self.data}'


class AcessoMedico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    identificacao = models.CharField(max_length=50)
    tempo_de_acesso = models.IntegerField() # Em horas
    criado_em = models.DateTimeField()
    data_exames_iniciais  = models.DateField()
    data_exames_finais = models.DateField()
    token = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.token
        #essa função serve para verificar se existe um token cadastrado no BD, caso não exista, o token será o token pela URL
        #esse token será criado automaticamente
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = token_urlsafe(6)

        super(AcessoMedico, self).save(*args, **kwargs)

    @property
    def status(self):
        return 'Expirado' if timezone.now() > (self.criado_em + timedelta(hours=self.tempo_de_acesso)) else 'Ativo'
   
    @property
    def url(self):
        return f'http://127.0.0.1:8000/exames/acesso_medico/{self.token}'
 
