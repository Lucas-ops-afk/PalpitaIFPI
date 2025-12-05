from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('ranking/', views.ranking_view, name='ranking'),
    path('jogos/', views.listar_jogos, name='listar_jogos'),
    path('jogos/modalidade/<int:modalidade_id>/', views.listar_jogos, name='jogos_por_modalidade'),
    path('jogos/<int:jogo_id>/palpitar/', views.criar_palpite, name='criar_palpite'),
    path('jogos/<int:jogo_id>/apostar/', views.apostar, name='apostar'),
    path('meus-palpites/', views.meus_palpites, name='meus_palpites'),
]
