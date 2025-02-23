from django.db import models
from django.contrib.auth.models import User


class Projects(models.Model):
    status_choices = [
        ('A', 'в процессе'),
        ('C', 'закрыт'),
        ('F', 'приостановлен')
    ]

    name = models.CharField(max_length=30)
    description = models.TextField()
    start = models.DateField()
    end = models.DateField()

    status = models.CharField(
        max_length=2,
        choices=status_choices,
        default='A'
    )
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects_manager',
    )

    class Meta:
        permissions = [
            ("manage_project", "Возможность управлять проектом")
        ]

    def __str__(self):
        return (f'Проект - {self.name}, дата начала - {self.start}, дата окончания - {self.end},\n'
                f'статус - {self.status}, менеджер проекта - {self.manager}')