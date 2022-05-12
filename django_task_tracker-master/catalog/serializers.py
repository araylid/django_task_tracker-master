from rest_framework import serializers
from catalog.models import User, Project, Description, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'author')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'purpose', 'project', 'status', 'author',
                  'worker', 'added_at')


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ('id', 'description', 'task', 'author', 'added_at')
