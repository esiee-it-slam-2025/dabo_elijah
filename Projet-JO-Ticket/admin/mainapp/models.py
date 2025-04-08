from django.db import models
from django.contrib.auth.models import User
import uuid

class Stadium(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} - {self.location}"

class Team(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)
    nickname = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Event(models.Model):
    start = models.DateTimeField()
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    team_home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_events', null=True, blank=True)
    team_away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_events', null=True, blank=True)
    
    def __str__(self):
        home_name = self.team_home.name if self.team_home else "À déterminer"
        away_name = self.team_away.name if self.team_away else "À déterminer"
        return f"{home_name} vs {away_name} - {self.start.strftime('%d/%m/%Y %H:%M')}"

class Ticket(models.Model):
    CATEGORY_CHOICES = [
        ('SILVER', 'Silver'),
        ('GOLD', 'Gold'),
        ('PLATINUM', 'Platinum'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Ticket {self.id} - {self.user.username} - {self.event}"
    
    def save(self, *args, **kwargs):
        if not self.price:
            if self.category == 'SILVER':
                self.price = 100
            elif self.category == 'GOLD':
                self.price = 200
            elif self.category == 'PLATINUM':
                self.price = 300
        
        super().save(*args, **kwargs)