from django.db import models
import uuid
from django.contrib.auth.models import User  # Importation du modèle utilisateur Django

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey('Match', on_delete=models.CASCADE)  # Lien vers un match (assure-toi que le modèle Match existe)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Lien vers l'utilisateur
    category = models.CharField(
        max_length=20,
        choices=[
            ('Silver', 'Silver'),
            ('Gold', 'Gold'),
            ('Platinum', 'Platinum')
        ]
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Prix du billet
    purchased_at = models.DateTimeField(auto_now_add=True)  # Date d'achat auto

    def __str__(self):
        return f"{self.user.username} - {self.match} ({self.category})"
