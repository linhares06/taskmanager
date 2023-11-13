from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from manager.models import Comment, Priority, Status, Tag, Task

CHAR_FIELD_CSS_CLASS = { 'class': 'form-control' }
SELECT_FIELD_CSS_CLASS = { 'class': 'form-select' }

def remove_first_element_from_combo(combobox):
    choices = list(combobox)
    choices.pop(0)
    return choices

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs=CHAR_FIELD_CSS_CLASS))
    email = forms.CharField(widget=forms.EmailInput(attrs=CHAR_FIELD_CSS_CLASS))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=CHAR_FIELD_CSS_CLASS))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=CHAR_FIELD_CSS_CLASS))

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs=CHAR_FIELD_CSS_CLASS))
    password = forms.CharField(widget=forms.PasswordInput(attrs=CHAR_FIELD_CSS_CLASS))

class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'status', 'assignee', 'priority', 'tags')
        widgets = {
            'title': forms.TextInput(attrs=CHAR_FIELD_CSS_CLASS),
            'description': forms.Textarea(attrs=CHAR_FIELD_CSS_CLASS),
            'due_date': forms.TextInput(attrs={ 'type': 'date', **CHAR_FIELD_CSS_CLASS })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(NewTaskForm, self).__init__(*args, **kwargs)
        self.fields["priority"].queryset = Priority.objects.filter(user=user)
        self.fields["status"].queryset = Status.objects.filter(user=user)
        self.fields["tags"].queryset = Tag.objects.filter(user=user)

        self.fields['status'].choices = remove_first_element_from_combo(self.fields['status'].choices)
        self.fields['priority'].choices = remove_first_element_from_combo(self.fields['priority'].choices)
        self.fields['assignee'].choices = remove_first_element_from_combo(self.fields['assignee'].choices)
        self.fields['assignee'].initial = user

        self.fields['priority'].widget.attrs.update(SELECT_FIELD_CSS_CLASS)
        self.fields['status'].widget.attrs.update(SELECT_FIELD_CSS_CLASS)
        self.fields['assignee'].widget.attrs.update(SELECT_FIELD_CSS_CLASS)    
        self.fields['tags'].widget.attrs.update(SELECT_FIELD_CSS_CLASS)

class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'status', 'assignee', 'priority', 'tags')
        widgets = {
            'title': forms.TextInput(attrs=CHAR_FIELD_CSS_CLASS),
            'description': forms.Textarea(attrs=CHAR_FIELD_CSS_CLASS),
            'due_date': forms.TextInput(attrs={ 'type': 'date', **CHAR_FIELD_CSS_CLASS })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(EditTaskForm, self).__init__(*args, **kwargs)
        self.fields['priority'].queryset = Priority.objects.filter(user=user)
        self.fields['status'].queryset = Status.objects.filter(user=user)
        self.fields['tags'].queryset = Tag.objects.filter(user=user)

        self.fields['status'].choices = remove_first_element_from_combo(self.fields['status'].choices)
        self.fields['priority'].choices = remove_first_element_from_combo(self.fields['priority'].choices)
        self.fields['assignee'].choices = remove_first_element_from_combo(self.fields['assignee'].choices)

        self.fields['priority'].widget.attrs.update(SELECT_FIELD_CSS_CLASS)
        self.fields['status'].widget.attrs.update(SELECT_FIELD_CSS_CLASS)
        self.fields['assignee'].widget.attrs.update(SELECT_FIELD_CSS_CLASS)    
        self.fields['tags'].widget.attrs.update(SELECT_FIELD_CSS_CLASS)

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class NewStatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ('name',)

class NewPriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ('name',)

class NewTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)

class SearchForm(forms.Form):

    title = forms.CharField(required=False, widget=forms.TextInput(attrs=CHAR_FIELD_CSS_CLASS))
    description = forms.CharField(required=False, widget=forms.TextInput(attrs=CHAR_FIELD_CSS_CLASS))
    due_date = forms.CharField(required=False, widget=forms.TextInput(attrs={ 'type': 'date', **CHAR_FIELD_CSS_CLASS }))
    assignee = forms.ChoiceField(required=False)
    status = forms.ChoiceField(required=False)
    priority = forms.ChoiceField(required=False)
    tag = forms.MultipleChoiceField(required=False)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['priority'].choices = self.get_choices(user, Priority)
        self.fields['priority'].widget.attrs.update(SELECT_FIELD_CSS_CLASS)

        self.fields['status'].choices = self.get_choices(user, Status)
        self.fields['status'].widget.attrs.update(SELECT_FIELD_CSS_CLASS)

        self.fields['tag'].choices = self.get_choices(user, Tag)
        self.fields['tag'].widget.attrs.update(SELECT_FIELD_CSS_CLASS)

        self.fields['assignee'].choices = self.get_choices(user, User)
        self.fields['assignee'].widget.attrs.update(SELECT_FIELD_CSS_CLASS)

    def get_choices(self, user, model):

        choices = []

        if model == User:
            assignees = list(Task.objects.filter(user_id=user).values_list('assignee', flat=True).distinct())
            choices = list(User.objects.filter(id__in=assignees).values_list('id', 'username'))
        else:
            choices = list(model.objects.filter(user_id=user).values_list('id', 'name'))
        
        choices.insert(0, ('', ''))

        if model == Status:
            choices.append((-1, 'Completed'))

        return choices