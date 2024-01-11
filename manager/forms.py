from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from manager.models import Comment, Priority, Status, Tag, Task

CHAR_FIELD_CSS_CLASS = { 'class': 'form-control' }
SELECT_FIELD_CSS_CLASS = { 'class': 'form-select' }

def remove_first_element_from_combo(combobox):
    """
    Removes the first element from a combobox and returns the modified list of choices.

    Args:
    - combobox: An iterable representing the choices in the combobox.

    Returns:
    - list: A list of choices with the first element removed.
    """
    choices = list(combobox)
    choices.pop(0)
    return choices

class SignupForm(UserCreationForm):
    """
    Custom form for user signup.

    Extends Django's built-in UserCreationForm to include additional styling for form fields.

    Attributes:
    - username: CharField - User's desired username.
    - email: CharField - User's email address.
    - password1: CharField - User's password.
    - password2: CharField - Confirmation of the user's password.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs=CHAR_FIELD_CSS_CLASS))
    email = forms.CharField(widget=forms.EmailInput(attrs=CHAR_FIELD_CSS_CLASS))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=CHAR_FIELD_CSS_CLASS))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=CHAR_FIELD_CSS_CLASS))

class LoginForm(AuthenticationForm):
    """
    Custom form for user login.

    Extends Django's built-in AuthenticationForm to include additional styling for form fields.

    Attributes:
    - username: CharField - User's username for authentication.
    - password: CharField - User's password for authentication.
    """
    username = forms.CharField(widget=forms.TextInput(attrs=CHAR_FIELD_CSS_CLASS))
    password = forms.CharField(widget=forms.PasswordInput(attrs=CHAR_FIELD_CSS_CLASS))

class NewTaskForm(forms.ModelForm):
    """
    Form for creating a new task.

    Extends Django's ModelForm for the Task model with customized widgets and additional logic
    to filter choices and set default values based on the user.

    Attributes:
    - title: CharField - Title of the task.
    - description: Textarea - Description of the task.
    - due_date: TextInput - Due date of the task (formatted as 'date').
    - status: ModelChoiceField - Status of the task.
    - assignee: ModelChoiceField - Assignee of the task.
    - priority: ModelChoiceField - Priority of the task.
    - tags: ModelMultipleChoiceField - Tags associated with the task.
    """
    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'status', 'assignee', 'priority', 'tags')
        widgets = {
            'title': forms.TextInput(attrs=CHAR_FIELD_CSS_CLASS),
            'description': forms.Textarea(attrs=CHAR_FIELD_CSS_CLASS),
            'due_date': forms.TextInput(attrs={ 'type': 'date', **CHAR_FIELD_CSS_CLASS })
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with additional logic for setting choices and default values.

        Args:
        - user: User object - The user for whom the form is being rendered.
        """
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
    """
    Form for editing an existing task.

    Extends Django's ModelForm for the Task model with customized widgets and additional logic
    to filter choices based on the user.

    Attributes:
    - title: CharField - Title of the task.
    - description: Textarea - Description of the task.
    - due_date: TextInput - Due date of the task (formatted as 'date').
    - status: ModelChoiceField - Status of the task.
    - assignee: ModelChoiceField - Assignee of the task.
    - priority: ModelChoiceField - Priority of the task.
    - tags: ModelMultipleChoiceField - Tags associated with the task.
    """
    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'status', 'assignee', 'priority', 'tags')
        widgets = {
            'title': forms.TextInput(attrs=CHAR_FIELD_CSS_CLASS),
            'description': forms.Textarea(attrs=CHAR_FIELD_CSS_CLASS),
            'due_date': forms.TextInput(attrs={ 'type': 'date', **CHAR_FIELD_CSS_CLASS })
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with additional logic for setting choices.

        Args:
        - user: User object - The user for whom the form is being rendered.
        """
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
    """
    Form for creating a new comment.

    Extends Django's ModelForm for the Comment model.

    Attributes:
    - content: Textarea - Content of the comment.
    """
    class Meta:
        model = Comment
        fields = ('content',)

class NewStatusForm(forms.ModelForm):
    """
    Form for creating a new status.

    Extends Django's ModelForm for the Status model.

    Attributes:
    - name: CharField - Name of the status.
    """
    class Meta:
        model = Status
        fields = ('name',)

class NewPriorityForm(forms.ModelForm):
    """
    Form for creating a new priority.

    Extends Django's ModelForm for the Priority model.

    Attributes:
    - name: CharField - Name of the priority.
    """
    class Meta:
        model = Priority
        fields = ('name',)

class NewTagForm(forms.ModelForm):
    """
    Form for creating a new tag.

    Extends Django's ModelForm for the Tag model.

    Attributes:
    - name: CharField - Name of the tag.
    """
    class Meta:
        model = Tag
        fields = ('name',)

class SearchForm(forms.Form):
    """
    Form for searching tasks based on various criteria.

    Attributes:
    - title: CharField - Task title for search.
    - description: CharField - Task description for search.
    - due_date: CharField - Due date for search (formatted as a date).
    - assignee: ChoiceField - Assignee for search.
    - status: ChoiceField - Task status for search.
    - priority: ChoiceField - Task priority for search.
    - tag: MultipleChoiceField - Task tags for search.
    """
    title = forms.CharField(required=False, widget=forms.TextInput(attrs=CHAR_FIELD_CSS_CLASS))
    description = forms.CharField(required=False, widget=forms.TextInput(attrs=CHAR_FIELD_CSS_CLASS))
    due_date = forms.CharField(required=False, widget=forms.TextInput(attrs={ 'type': 'date', **CHAR_FIELD_CSS_CLASS }))
    assignee = forms.ChoiceField(required=False)
    status = forms.ChoiceField(required=False)
    priority = forms.ChoiceField(required=False)
    tag = forms.MultipleChoiceField(required=False)
    
    def __init__(self, *args, **kwargs):
        """
        Constructor for the SearchForm.

        Parameters:
        - user: User - The user for whom the form is being rendered.
        """
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
        """
        Retrieve choices based on the specified user and model.

        Args:
        - user: The user for whom choices are being retrieved.
        - model: The Django model class for which choices are being retrieved.

        Returns:
        - list: A list of tuples representing choices. Each tuple contains two elements:
        - The first element is the ID of the choice.
        - The second element is the display name of the choice.

        Example:
        For a User model:
        >>> get_choices(user_instance, User)
        [(1, 'username1'), (2, 'username2'), ...]

        For other models:
        >>> get_choices(user_instance, AnotherModel)
        [(1, 'name1'), (2, 'name2'), ...]

        Special Handling:
        - Inserts an empty choice at the beginning of the list.
        - If the model is Status, appends a special choice for 'Completed' with ID -1.
        """
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