from django.db import models
from inventory.models import ClassModel


class Client(ClassModel):
    TYPES = (
        ('natural', 'Natural'),
        ('juridical', 'Juridical'),

    )
    name = models.CharField(
        max_length=100
    )
    lastname = models.CharField(
        max_length=100
    )
    movil = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    type_client = models.CharField(
        max_length=10,
        choices=TYPES,
        default='natural'
    )

    def __str__(self):
        return f"{self.lastname} { self.name}"

    def save(self):
        self.name = self.name.upper()
        self.lastname = self.lastname.upper()
        super(Client, self).save()

    class Meta:
        verbose_name_plural = "Clients"
