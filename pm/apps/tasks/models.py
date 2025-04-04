from django.db import models
from ..projects.models import Projects
from django.contrib.auth.models import User

class Tasks(models.Model):
    priority_choices = [
        ('H', 'Высокий'),
        ('M', 'Средний'),
        ('L', 'Низкий')
    ]
    status_choices = [
        ('N', 'Не начато'),
        ('I', 'В процессе'),
        ('C', 'Завершено'),
    ]

    name = models.CharField(max_length=30)
    description = models.TextField()
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    priority = models.CharField(
        max_length=2,
        choices=priority_choices,
        default='H'
    )
    status = models.CharField(
        max_length=2,
        choices=status_choices,
        default='N'
    )
    start = models.DateField()
    end = models.DateField()
    '''
    в переменной ниже Tasks будет обращаться к определенному пользователю executor, 
    чтобы один пользователь мог назначаться испольнителем сразу нескольких задач.
    '''
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks_executor',
                                 )

    class Meta:
        permissions = [
            ("view_assigned_task", "возможность просматривать задачу")
        ]

    def __str__(self):
        return (f'В проекте {self.project} задача - {self.name}, приоритет - {self.priority}, статус - {self.status},\n'
                f' начало - {self.start}, конец - {self.end}\n'
                f'исполнитель - {self.executor}')