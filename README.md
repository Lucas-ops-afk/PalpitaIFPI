# 🏆 PalpitaIFPI

Sistema de palpites e apostas esportivas para as modalidades do IFPI, inspirado no modelo Bet365.

## 📋 Descrição

O PalpitaIFPI é uma plataforma web desenvolvida em Django que permite aos usuários fazerem palpites e apostas em jogos esportivos das modalidades do IFPI (Futsal, Handball, etc.). O sistema inclui:

- Sistema de apostas com odds (1X2 e Placar Exato)
- Sistema de XP e níveis
- Ranking de jogadores
- Interface moderna com tema verde e preto
- Layout inspirado na Bet365

## 🚀 Tecnologias

- **Django 5.2.8**
- **Python 3.12+**
- **SQLite** (desenvolvimento)
- **Django REST Framework**

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/PalpitaIFPI.git
cd PalpitaIFPI
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv myvenv
# Windows
myvenv\Scripts\activate
# Linux/Mac
source myvenv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações:
```bash
python manage.py migrate
```

5. Crie um superusuário:
```bash
python manage.py createsuperuser
```

6. Execute o servidor:
```bash
python manage.py runserver
```

## 🎮 Funcionalidades

### Sistema de Apostas
- Apostas em resultado 1X2 (Time 1, Empate, Time 2)
- Apostas em placar exato
- Cálculo automático de ganhos baseado em odds
- Histórico de apostas

### Sistema de XP
- Ganho de XP ao acertar palpites
- Sistema de níveis baseado em XP
- Ranking dos melhores jogadores

### Administração
- Interface admin do Django para gerenciar:
  - Modalidades esportivas
  - Jogos e resultados
  - Odds dos jogos
  - Apostas dos usuários

## 📁 Estrutura do Projeto

```
PalpitaIFPI/
├── bets/                 # App principal
│   ├── models.py        # Modelos (Perfil, Jogo, Aposta, etc.)
│   ├── views.py         # Views do sistema
│   ├── urls.py          # URLs do app
│   ├── signals.py       # Signals para processar apostas
│   └── templates/       # Templates HTML
├── palpitaifpi/         # Configurações do projeto
│   ├── settings.py      # Configurações Django
│   └── urls.py          # URLs principais
├── requirements.txt     # Dependências
└── manage.py           # Script de gerenciamento Django
```

## 🎯 Como Usar

1. **Criar Modalidades**: Acesse `/admin/` e crie modalidades esportivas
2. **Criar Jogos**: Adicione jogos com times, data e odds
3. **Fazer Apostas**: Usuários podem apostar em jogos futuros
4. **Finalizar Jogos**: Preencha o placar final no admin para processar apostas automaticamente

## 📊 Sistema de Pontuação

- **Placar Exato**: 50 pontos de XP
- **Acertar Vencedor/Empate**: 10 pontos de XP
- **Sistema de Níveis**: Baseado em XP acumulado

## 🔒 Segurança

⚠️ **Importante**: Antes de fazer deploy em produção:
- Altere a `SECRET_KEY` no `settings.py`
- Configure `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Use variáveis de ambiente para dados sensíveis

## 📝 Licença

Este projeto é desenvolvido para uso educacional no IFPI.

## 👥 Contribuidores

- Desenvolvido para o IFPI

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

