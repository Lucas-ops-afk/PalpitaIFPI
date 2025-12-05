from django.contrib import admin
from .models import Modalidade, Jogo, Palpite, Perfil, Aposta, Medalha

# Admin para Medalha
@admin.register(Medalha)
class MedalhaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'imagem', 'descricao')

@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ('time1','time2','modalidade','data','odd_time1','odd_empate','odd_time2','finalizado')
    list_filter = ('modalidade','finalizado')
    fieldsets = (
        ('Informações do Jogo', {
            'fields': ('modalidade', 'time1', 'time2', 'data', 'finalizado')
        }),
        ('Placar Final', {
            'fields': ('placar_time1', 'placar_time2')
        }),
        ('Odds', {
            'fields': ('odd_time1', 'odd_empate', 'odd_time2', 'odd_placar_exato')
        }),
    )

@admin.register(Aposta)
class ApostaAdmin(admin.ModelAdmin):
    list_display = ('usuario','jogo','tipo','aposta_1x2','palpite_time1','palpite_time2','criado_em')
    list_filter = ('tipo','criado_em')
    readonly_fields = ('criado_em','atualizado_em')
    search_fields = ('usuario__username','jogo__time1','jogo__time2')

@admin.register(Palpite)
class PalpiteAdmin(admin.ModelAdmin):
    list_display = ('usuario','jogo','palpite_time1','palpite_time2','pontos','calculado')

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user','xp','nivel')
    readonly_fields = ('xp','nivel')
    filter_horizontal = ('medalhas',)