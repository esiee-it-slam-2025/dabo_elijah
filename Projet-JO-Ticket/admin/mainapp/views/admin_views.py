from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from ..models import Event, Team, Stadium

@staff_member_required
def admin_matches(request):
    """
    Vue pour l'interface d'administration des matchs.
    Permet de modifier la date, le stade, les équipes et les scores des matchs.
    """
    events = Event.objects.all().order_by('start')
    teams = Team.objects.all().order_by('name')
    stadiums = Stadium.objects.all().order_by('name')
    
    if request.method == 'POST':
        try:
            for event in events:
                # Récupérer les données du formulaire pour chaque match
                start = request.POST.get(f'start_{event.id}')
                team_home_id = request.POST.get(f'team_home_{event.id}')
                team_away_id = request.POST.get(f'team_away_{event.id}')
                score_home = request.POST.get(f'score_home_{event.id}')
                score_away = request.POST.get(f'score_away_{event.id}')
                stadium_id = request.POST.get(f'stadium_{event.id}')
                
                # Mettre à jour l'événement
                if start:
                    try:
                        event.start = timezone.make_aware(timezone.datetime.fromisoformat(start))
                    except (ValueError, TypeError):
                        # Gérer les erreurs de format de date
                        pass
                
                # Gérer les équipes (peut être None pour les matchs futurs)
                if team_home_id and team_home_id != '':
                    event.team_home_id = team_home_id
                
                if team_away_id and team_away_id != '':
                    event.team_away_id = team_away_id
                
                # Mettre à jour le stade
                if stadium_id and stadium_id != '':
                    event.stadium_id = stadium_id
                
                # Gérer les scores
                if score_home is not None and score_away is not None and score_home != '' and score_away != '':
                    event.score = f"{score_home}-{score_away}"
                    
                    # Déterminer le vainqueur (seulement si les deux équipes sont assignées)
                    if event.team_home and event.team_away:
                        try:
                            if int(score_home) > int(score_away):
                                event.winner = event.team_home
                            elif int(score_home) < int(score_away):
                                event.winner = event.team_away
                            else:
                                event.winner = None  # Match nul
                        except (ValueError, TypeError):
                            # Gérer les erreurs de conversion des scores
                            pass
                
                # Sauvegarder les modifications
                event.save()
            
            messages.success(request, 'Les matchs ont été mis à jour avec succès!')
            return redirect('admin_matches')
        
        except Exception as e:
            messages.error(request, f'Erreur lors de la mise à jour : {str(e)}')
    
    # Ajouter des attributs score_home et score_away pour faciliter l'affichage
    for event in events:
        if event.score:
            try:
                scores = event.score.split('-')
                event.score_home = scores[0].strip()
                event.score_away = scores[1].strip()
            except (IndexError, AttributeError):
                event.score_home = ''
                event.score_away = ''
        else:
            event.score_home = ''
            event.score_away = ''
    
    context = {
        'events': events,
        'teams': teams,
        'stadiums': stadiums,
    }
    
    return render(request, 'admin_matches.html', context)