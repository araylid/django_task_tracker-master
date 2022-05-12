from django.forms import ModelForm, Form
from django import forms
from catalog.models import Task, Description, Project, User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User



class DateInput(forms.DateInput):
    input_type = 'date'


class CreateNewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['purpose', 'project', 'status', 'worker', 'deadline']
        labels = {
            'purpose': 'Цель',
            'project': 'Проект',
            'status': 'Статус',
            'worker': 'Исполнитель',
            'author': 'Автор',
            'deadline': 'Дедлайн',
        }
        widgets = {
            'deadline': DateInput(),
            }



class FilterTaskForm(Form):
    project = forms.ModelChoiceField(Project.objects.all(), required=False)
    status = forms.ChoiceField(choices=(
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Ready', 'Ready'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
        ('Being tested', 'Being tested'),
        (None, '---------')), required=False)
    search_text = forms.CharField(max_length=150, required=False)


class CreateNewDescriptionForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ['description', ]
        labels = {
            'description': 'Комментарий',
            'author': 'You are',
        }


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'worker', 'deadline']
        labels = {
            'status': 'Новый статус',
            'worker': 'Новый исполнитель',
            'deadline': 'Дедлайн'
        }
        widgets = {
            'deadline': DateInput(),
            }

class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class DateForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])