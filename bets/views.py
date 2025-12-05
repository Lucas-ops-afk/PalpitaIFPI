from django.contrib.auth import logout as auth_logout

def logout_view(request):
    auth_logout(request)
    return redirect('login')
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        errors = {}
        if not username or not email or not password1 or not password2:
            errors['fields'] = 'Preencha todos os campos.'
        if password1 != password2:
            errors['password'] = 'As senhas não coincidem.'
        if User.objects.filter(username=username).exists():
            errors['username'] = 'Usuário já existe.'
        if User.objects.filter(email=email).exists():
            errors['email'] = 'E-mail já cadastrado.'
        if errors:
            return render(request, 'register.html', {'form': errors})
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        user = authenticate(request, username=username, password=password1)
        if user:
            auth_login(request, user)
            return redirect('listar_jogos')
    return render(request, 'register.html', {'form': {}})

# IMPORTS (mover para o topo do arquivo se necessário)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Perfil, Jogo, Modalidade, Palpite, Aposta, TipoAposta, Medalha
from django.db.models import Q

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        auth_login(request, user)
        if user.is_superuser:
            return redirect('/admin/')
        return redirect('listar_jogos')
    return render(request, 'login.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Perfil, Jogo, Modalidade, Palpite, Aposta, TipoAposta
from django.db.models import Q
from decimal import Decimal

@login_required
def home(request):
    """Página inicial com informações sobre o sistema"""
    modalidades = Modalidade.objects.all()
    jogos_proximos = Jogo.objects.filter(
        data__gte=timezone.now(),
        finalizado=False
    ).order_by('data')[:5]
    
    context = {
        'modalidades': modalidades,
        'jogos_proximos': jogos_proximos,
    }
    return render(request, 'home.html', context)

@login_required
def ranking_view(request):
    """Exibe o ranking de jogadores por XP e todas as medalhas do sistema"""
    top = Perfil.objects.select_related('user').order_by('-xp')[:50]
    medalhas = Medalha.objects.all()
    return render(request, 'ranking.html', {'top': top, 'medalhas': medalhas})

@login_required
def listar_jogos(request, modalidade_id=None):
    """Lista todos os jogos, opcionalmente filtrados por modalidade"""
    jogos = Jogo.objects.select_related('modalidade').all()
    
    if modalidade_id:
        modalidade = get_object_or_404(Modalidade, id=modalidade_id)
        jogos = jogos.filter(modalidade=modalidade)
    else:
        modalidade = None
    
    # Separar jogos por status
    jogos_futuros = jogos.filter(data__gte=timezone.now(), finalizado=False).order_by('data')
    jogos_passados = jogos.filter(
        Q(data__lt=timezone.now()) | Q(finalizado=True)
    ).order_by('-data')
    
    modalidades = Modalidade.objects.all()
    
    context = {
        'jogos_futuros': jogos_futuros,
        'jogos_passados': jogos_passados,
        'modalidades': modalidades,
        'modalidade_selecionada': modalidade,
    }
    return render(request, 'jogos/listar.html', context)

@login_required
def criar_palpite(request, jogo_id):
    """Permite ao usuário criar um palpite para um jogo"""
    jogo = get_object_or_404(Jogo, id=jogo_id)
    
    # Verificar se o jogo já passou ou está finalizado
    if jogo.finalizado or jogo.data < timezone.now():
        messages.error(request, 'Não é possível palpitar em jogos que já foram finalizados!')
        return redirect('listar_jogos')
    
    # Verificar se já existe palpite
    palpite_existente = Palpite.objects.filter(usuario=request.user, jogo=jogo).first()
    
    if request.method == 'POST':
        palpite_time1 = request.POST.get('palpite_time1')
        palpite_time2 = request.POST.get('palpite_time2')
        
        try:
            palpite_time1 = int(palpite_time1)
            palpite_time2 = int(palpite_time2)
            
            if palpite_time1 < 0 or palpite_time2 < 0:
                messages.error(request, 'Os placares não podem ser negativos!')
            else:
                if palpite_existente:
                    # Atualizar palpite existente
                    palpite_existente.palpite_time1 = palpite_time1
                    palpite_existente.palpite_time2 = palpite_time2
                    palpite_existente.save()
                    messages.success(request, 'Palpite atualizado com sucesso!')
                else:
                    # Criar novo palpite
                    Palpite.objects.create(
                        usuario=request.user,
                        jogo=jogo,
                        palpite_time1=palpite_time1,
                        palpite_time2=palpite_time2
                    )
                    messages.success(request, 'Palpite criado com sucesso!')
                
                return redirect('listar_jogos')
        except ValueError:
            messages.error(request, 'Por favor, insira valores numéricos válidos!')
    
    context = {
        'jogo': jogo,
        'palpite_existente': palpite_existente,
    }
    return render(request, 'jogos/criar_palpite.html', context)

@login_required
def meus_palpites(request):
    """Lista todos os palpites do usuário logado"""
    palpites = Palpite.objects.filter(
        usuario=request.user
    ).select_related('jogo', 'jogo__modalidade').order_by('-criado_em')
    
    # Estatísticas
    total_palpites = palpites.count()
    total_pontos = sum(p.pontos for p in palpites)
    palpites_certos = palpites.filter(pontos__gt=0).count()
    
    # Obter ou criar perfil
    perfil, created = Perfil.objects.get_or_create(user=request.user)
    
    context = {
        'palpites': palpites,
        'total_palpites': total_palpites,
        'total_pontos': total_pontos,
        'palpites_certos': palpites_certos,
        'perfil': perfil,
    }
    return render(request, 'palpites/meus_palpites.html', context)

@login_required
def apostar(request, jogo_id):
    """Sistema tipo Bet365 - Criar aposta com odds e valores"""
    jogo = get_object_or_404(Jogo, id=jogo_id)
    perfil, created = Perfil.objects.get_or_create(user=request.user)
    
    # Verificar se o jogo já passou ou está finalizado
    if jogo.finalizado or jogo.data < timezone.now():
        messages.error(request, 'Não é possível apostar em jogos que já foram finalizados!')
        return redirect('listar_jogos')
    
    if request.method == 'POST':
        tipo_aposta = request.POST.get('tipo_aposta')
        
        try:
            aposta_1x2 = None
            palpite_time1 = None
            palpite_time2 = None
            
            if tipo_aposta == TipoAposta.RESULTADO_1X2:
                aposta_1x2 = request.POST.get('aposta_1x2')
                if aposta_1x2 not in ['1', 'X', '2']:
                    messages.error(request, 'Selecione uma opção válida!')
                    return redirect('apostar', jogo_id=jogo.id)
            
            elif tipo_aposta == TipoAposta.PLACAR_EXATO:
                palpite_time1 = int(request.POST.get('palpite_time1', 0))
                palpite_time2 = int(request.POST.get('palpite_time2', 0))
                
                if palpite_time1 < 0 or palpite_time2 < 0:
                    messages.error(request, 'Os placares não podem ser negativos!')
                    return redirect('apostar', jogo_id=jogo.id)
            
            # Criar aposta
            aposta = Aposta.objects.create(
                usuario=request.user,
                jogo=jogo,
                tipo=tipo_aposta,
                aposta_1x2=aposta_1x2,
                palpite_time1=palpite_time1,
                palpite_time2=palpite_time2
            )
            
            messages.success(request, 'Aposta criada com sucesso!')
            return redirect('meus_palpites')
            
        except (ValueError, TypeError) as e:
            messages.error(request, 'Por favor, insira valores válidos!')
    
    context = {
        'jogo': jogo,
        'perfil': perfil,
    }
    return render(request, 'apostas/apostar.html', context)

