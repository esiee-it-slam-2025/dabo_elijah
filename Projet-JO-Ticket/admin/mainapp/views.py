from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Stadium, Team, Event, Ticket
import json

# Fonction utilitaire pour sérialiser un objet Stadium
def serialize_stadium(stadium):
    return {
        'id': stadium.id,
        'name': stadium.name,
        'location': stadium.location,
    }

# Fonction utilitaire pour sérialiser un objet Team
def serialize_team(team):
    return {
        'id': team.id,
        'name': team.name,
        'code': team.code,
        'nickname': team.nickname,
    }

# Fonction utilitaire pour sérialiser un objet Event
def serialize_event(event):
    return {
        'id': event.id,
        'start': event.start.isoformat(),
        'stadium': serialize_stadium(event.stadium),
        'team_home': serialize_team(event.team_home) if event.team_home else None,
        'team_away': serialize_team(event.team_away) if event.team_away else None,
        'score': event.score,  # Ajout du score
        'winner': serialize_team(event.winner) if event.winner else None  # Ajout du vainqueur
    }
# Fonction utilitaire pour sérialiser un objet User
def serialize_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }

# Fonction utilitaire pour sérialiser un objet Ticket
def serialize_ticket(ticket):
    return {
        'id': str(ticket.id),
        'user': serialize_user(ticket.user),
        'event': serialize_event(ticket.event),
        'category': ticket.category,
        'price': float(ticket.price),
        'purchase_date': ticket.purchase_date.isoformat(),
        'is_used': ticket.is_used,
    }

# Générer un token CSRF
@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

# API: Stades
@api_view(['GET'])
@permission_classes([AllowAny])
def stadiums_list(request):
    stadiums = Stadium.objects.all()
    data = [serialize_stadium(stadium) for stadium in stadiums]
    return Response(data)

# API: Équipes
@api_view(['GET'])
@permission_classes([AllowAny])
def teams_list(request):
    teams = Team.objects.all()
    data = [serialize_team(team) for team in teams]
    return Response(data)

# API: Événements
@api_view(['GET'])
@permission_classes([AllowAny])
def events_list(request):
    events = Event.objects.all().order_by('start')
    data = [serialize_event(event) for event in events]
    return Response(data)

# API: Inscription utilisateur
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return Response({'message': 'Veuillez fournir tous les champs requis'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'message': 'Ce nom d\'utilisateur est déjà pris'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'message': 'Cet email est déjà utilisé'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        login(request, user)
        
        return Response({
            'message': 'Inscription réussie',
            'user': serialize_user(user)
        })
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API: Connexion utilisateur
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return Response({'message': 'Veuillez fournir l\'email et le mot de passe'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Email ou mot de passe incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = authenticate(username=user.username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({
                'message': 'Connexion réussie',
                'user': serialize_user(user)
            })
        else:
            return Response({'message': 'Email ou mot de passe incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vérifier si l'utilisateur est un superutilisateur
def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def match_admin(request):
    events = Event.objects.all().order_by('start')
    teams = Team.objects.all().order_by('name')
    stadiums = Stadium.objects.all()
    
    if request.method == 'POST':
        # Sauvegarde d'un seul événement
        if 'save_event' in request.POST:
            event_id = request.POST.get('save_event')
            update_event(request, event_id)
            messages.success(request, f'Match #{event_id} mis à jour avec succès.')
            return redirect('match_admin')
        
        # Sauvegarde de tous les événements
        elif 'save_all' in request.POST:
            for event in events:
                update_event(request, event.id)
            messages.success(request, 'Tous les matchs ont été mis à jour avec succès.')
            return redirect('match_admin')
    
    return render(request, 'admin/match_admin.html', {
        'events': events,
        'teams': teams,
        'stadiums': stadiums,
    })

def update_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        
        # Mise à jour de la date et heure
        datetime_str = request.POST.get(f'datetime_{event_id}')
        if datetime_str:
            from django.utils import timezone
            import datetime
            # Convertir la chaîne datetime en objet datetime
            event.start = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
            # Si on utilise TIME_ZONE dans settings, s'assurer qu'on est en UTC
            # event.start = timezone.make_aware(event.start)
        
        # Mise à jour des équipes
        team_home_id = request.POST.get(f'team_home_{event_id}')
        if team_home_id:
            event.team_home_id = team_home_id
        else:
            event.team_home = None
            
        team_away_id = request.POST.get(f'team_away_{event_id}')
        if team_away_id:
            event.team_away_id = team_away_id
        else:
            event.team_away = None
        
        # Mise à jour du score
        score_home = request.POST.get(f'score_home_{event_id}')
        score_away = request.POST.get(f'score_away_{event_id}')
        if score_home and score_away:
            event.score = f"{score_home}-{score_away}"
            
            # Déterminer le vainqueur
            if int(score_home) > int(score_away):
                event.winner = event.team_home
            elif int(score_away) > int(score_home):
                event.winner = event.team_away
            else:
                event.winner = None
        else:
            event.score = None
            event.winner = None
        
        # Mise à jour du stade
        stadium_id = request.POST.get(f'stadium_{event_id}')
        if stadium_id:
            event.stadium_id = stadium_id
        
        event.save()
        return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour du match #{event_id}: {str(e)}")
        return False

# API: Déconnexion utilisateur
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Déconnexion réussie'})

# API: Achat de billet
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def buy_ticket(request):
    try:
        data = json.loads(request.body)
        event_id = data.get('event_id')
        category = data.get('category', '').upper()
        quantity = int(data.get('quantity', 1))
        
        if not event_id or not category:
            return Response({'message': 'Veuillez fournir l\'ID de l\'événement et la catégorie'}, status=status.HTTP_400_BAD_REQUEST)
        
        if category not in ['SILVER', 'GOLD', 'PLATINUM']:
            return Response({'message': 'Catégorie invalide'}, status=status.HTTP_400_BAD_REQUEST)
        
        if quantity < 1 or quantity > 10:
            return Response({'message': 'La quantité doit être comprise entre 1 et 10'}, status=status.HTTP_400_BAD_REQUEST)
        
        event = get_object_or_404(Event, id=event_id)
        
        # Prix selon la catégorie
        price = {
            'SILVER': 100,
            'GOLD': 200,
            'PLATINUM': 300
        }[category]
        
        tickets = []
        
        for _ in range(quantity):
            ticket = Ticket.objects.create(
                user=request.user,
                event=event,
                category=category,
                price=price
            )
            tickets.append(serialize_ticket(ticket))
        
        return Response({
            'message': f"{quantity} billet(s) acheté(s) avec succès",
            'tickets': tickets
        })
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API: Liste des billets de l'utilisateur connecté
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-purchase_date')
    data = [serialize_ticket(ticket) for ticket in tickets]
    return Response(data)

# API: Informations sur un billet spécifique
@api_view(['GET'])
@permission_classes([AllowAny])
def get_ticket_info(request, ticket_id):
    try:
        ticket = get_object_or_404(Ticket, id=ticket_id)
        return Response(serialize_ticket(ticket))
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API: Valider un billet (marquer comme utilisé)
@api_view(['POST'])
@permission_classes([AllowAny])
def validate_ticket(request, ticket_id):
    try:
        ticket = get_object_or_404(Ticket, id=ticket_id)
        
        if ticket.is_used:
            return Response({'message': 'Ce billet a déjà été utilisé'}, status=status.HTTP_400_BAD_REQUEST)
        
        ticket.is_used = True
        ticket.save()
        
        return Response({
            'message': 'Billet validé avec succès',
            'ticket': serialize_ticket(ticket)
        })
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)