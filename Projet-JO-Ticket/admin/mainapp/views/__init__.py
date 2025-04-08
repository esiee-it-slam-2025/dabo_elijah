# Import des vues de l'API
from .api import (
    get_csrf_token,
    stadiums_list,
    teams_list,
    events_list,
    register,
    login_view,
    logout_view,
    buy_ticket,
    user_tickets,
    get_ticket_info,
    validate_ticket
)

# Import des vues d'administration
from .admin_views import admin_matches

__all__ = [
    'get_csrf_token',
    'stadiums_list',
    'teams_list',
    'events_list',
    'register',
    'login_view',
    'logout_view',
    'buy_ticket',
    'user_tickets',
    'get_ticket_info',
    'validate_ticket',
    'admin_matches'
]