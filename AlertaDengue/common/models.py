from django.db import models


class FederatedState(models.Model):
    """
    geocode INT NOT NULL,
    name VARCHAR NOT NULL,
    state VARCHAR NOT NULL,
    status BOOL NOT NULL,

    """

    STATUS_CHOICES = [
        (True, 'Enable'),
        (False, 'Disable'),
    ]

    geocode = models.IntegerField(
        db_column='geocodigo',
        null=False,
        primary_key=True,
        help_text='Código do Município',
    )
    name = models.CharField(
        db_column='nome',
        null=False,
        max_length=128,
        help_text='Nome do municipio',
    )
    state = models.CharField(
        db_column='uf', null=False, max_length=20, help_text='Nome do estado',
    )
    status = models.BooleanField(db_column='status', choices=STATUS_CHOICES)

    class Meta:
        db_table = 'Dengue_global\".\"estado'
        app_label = 'dados'
        verbose_name_plural = "Federated State"

    def __str__(self):
        return self.name
