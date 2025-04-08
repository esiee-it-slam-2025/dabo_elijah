from django.db import models


class Event(models.Model):
    stadium = models.ForeignKey("Stadium", on_delete=models.PROTECT)
    team_home = models.ForeignKey("Team", on_delete=models.PROTECT, null=True, blank=True, related_name="events_as_home")
    team_away = models.ForeignKey("Team", on_delete=models.PROTECT, null=True, blank=True, related_name="events_as_away")
    start = models.DateTimeField()
    score = models.CharField(max_length=10, blank=True, null=True)
    winner = models.ForeignKey("Team", on_delete=models.PROTECT, null=True, blank=True, related_name="events_winner")

    def __str__(self):
        home_name = self.team_home.name if self.team_home else "À déterminer"
        away_name = self.team_away.name if self.team_away else "À déterminer"
        return f"{home_name} vs {away_name} - {self.start.strftime('%d/%m/%Y %H:%M')}"