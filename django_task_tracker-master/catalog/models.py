from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User as kekUser
from datetime import date


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])


class Project(models.Model):
    name = models.CharField(max_length=30)
    author = models.ForeignKey(kekUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])


class Task(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Ready', 'Ready'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
        ('Being tested', 'Being tested')
    )
    purpose = models.TextField(max_length=150)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    author = models.ForeignKey(kekUser, on_delete=models.CASCADE,
                               verbose_name="author", blank=True, null=True)
    worker = models.ForeignKey(kekUser, on_delete=models.CASCADE,
                               related_name="worker", blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()

    def __str__(self):
        return self.purpose

    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.id)])

    @property
    def is_past_due(self):
        return date.today() > self.deadline


class Description(models.Model):
    description = models.TextField(max_length=500)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments_tasks')
    author = models.ForeignKey(kekUser, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('description-detail', args=[str(self.id)])
