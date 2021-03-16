from django.db import models


class FederatedState(models.Model):
    STATUS_CHOICES = [
        (True, 'Enable'),
        (False, 'Disable'),
    ]
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=5)
    map_center_x = models.FloatField()
    map_center_y = models.FloatField()
    map_zoom = models.CharField(max_length=3)
    status = models.BooleanField(choices=STATUS_CHOICES)

    class Meta:
        app_label = 'common'
        verbose_name_plural = "Federated State"

    def __str__(self):
        return self.name
