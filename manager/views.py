from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F, ProtectedError, Count
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime, timedelta, date

from manager.models import Comment, Task, Tag, Priority, Status
from .forms import EditTaskForm, NewCommentForm, NewPriorityForm, NewStatusForm, NewTagForm, SearchForm, SignupForm, NewTaskForm
from .analytics.plot_generator import PlotGenerator

UPCOMMING_DUE_DATE_VALUE = 3
OVERDUE_DATE_VALUE = 0
CONFIGURATION_STATUS_OBJECT = 1
CONFIGURATION_PRIORITY_OBJECT = 2
CONFIGURATION_TAG_OBJECT = 3

def get_overdue_tasks(tasks):
    overdue_tasks = tasks.filter(
        completed=False,
        due_date__lt=date.today() + timedelta(days=OVERDUE_DATE_VALUE)
    ).values('id', 'title', 'due_date').order_by('due_date')
    
    return overdue_tasks

def get_upcomming_tasks(tasks):
    upcoming_tasks = tasks.filter(
        completed=False,
        due_date__gte=date.today() + timedelta(days=OVERDUE_DATE_VALUE),
        due_date__lte=date.today() + timedelta(days=UPCOMMING_DUE_DATE_VALUE)
    ).values('id', 'title', 'due_date').order_by('due_date')
    
    return upcoming_tasks

def generate_task_per_day_plot(tasks):
    today = datetime.now().date()
    start_date = today - timedelta(days=30)  # Assuming a 30-day period
    
    task_counts = tasks.filter(
        completed=True,
        completed_at__gte=start_date,
        completed_at__lte=today
    ).values('completed_at').annotate(count=Count('id'))

    dates = [entry['completed_at'] for entry in task_counts]
    counts = [entry['count'] for entry in task_counts]

    return PlotGenerator().generate_task_per_day(dates, counts)

def generate_task_by_status_plot(tasks):
    task_status_counts = tasks.values('status__name').annotate(count=Count('id'))

    status = [entry['status__name'] for entry in task_status_counts]
    counts = [entry['count'] for entry in task_status_counts]

    return PlotGenerator().generate_task_by_status(status, counts)

def generate_task_duration_plot(tasks):
    
    durations = tasks.filter(completed=True).annotate(duration=F('completed_at') - F('created_at')).values_list('duration', 'title')

    duration_list, title_list = zip(*[(duration.days, title) for duration, title in durations])

    return PlotGenerator().generate_task_duration([days + 1 for days in duration_list], title_list)

def generate_assignee_productivity_plot(tasks):
    
    results = tasks.filter(completed=True).values('assignee__username').annotate(
        completed_tasks=Count('id'),
    ) 
    
    assignees = [entry['assignee__username'] for entry in results]
    completed_tasks = [entry['completed_tasks'] for entry in results]

    return PlotGenerator().generate_assignee_productivity(assignees, completed_tasks)

def index(request):
    if request.user:
        return render(request, 'index.html')
    else:
        return render(request, 'home.html')

def logout(request):
    logout(request)
    return render(request, '/')

def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {
        'form': form
    })

@login_required
def home(request):
    tasks = Task.objects.filter(Q(user=request.user) | Q(assignee=request.user))

    total_tasks = tasks.count()
    total_completed = tasks.filter(completed=True).count()
    completion_rate = round(total_completed / total_tasks * 100, 2) if total_tasks != 0 else 0

    upcoming_tasks = get_upcomming_tasks(tasks)
    overdue_tasks = get_overdue_tasks(tasks)

    tasks_by_status = generate_task_by_status_plot(tasks)

    #Plots that need at least one task completed:
    tasks_per_day = None
    tasks_duration = None
    assignee_productivity_bar = None
    assignee_productivity_pie = None

    if total_completed > 0:
        tasks_per_day = generate_task_per_day_plot(tasks)
        tasks_duration = generate_task_duration_plot(tasks)
        assignee_productivity_bar, assignee_productivity_pie = generate_assignee_productivity_plot(tasks)
                                                                    
    context = {
        'completion_rate': completion_rate,
        'total_completed': total_completed,
        'total_tasks': total_tasks,
        'upcoming_tasks': upcoming_tasks,
        'overdue_tasks': overdue_tasks,
        'tasks_per_day': tasks_per_day,
        'tasks_by_status': tasks_by_status,
        'tasks_duration': tasks_duration,
        'assignee_productivity_bar': assignee_productivity_bar,
        'assignee_productivity_pie': assignee_productivity_pie,
    }

    # Render the template and pass the context
    return render(request, 'home.html', context)

@login_required
def list(request):
    ROWS_PER_PAGE = 15

    tasks = Task.objects.filter(Q(user=request.user) | Q(assignee=request.user)).order_by('created_at')
    paginator = Paginator(tasks, ROWS_PER_PAGE) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list.html', {
        'tasks': page_obj,
    })

@login_required
def new(request):

    if request.method == 'POST':
        form = NewTaskForm(request.POST, user=request.user)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user

            form.save()

            return redirect('manager:list')
    else:
        form = NewTaskForm(user=request.user)
        
    return render(request, 'form.html', {
        'form': form,
        'title': 'New Task',
    })

@login_required
def edit(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if task.user == request.user:
        # User is authorized to perform the action
        if request.method == 'POST':
            form = EditTaskForm(request.POST, instance=task, user=request.user)

            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user

                task.save()
                form.save_m2m()

                return redirect('manager:detail', pk=pk)
        else:
            form = EditTaskForm(instance=task, user=request.user)

        return render(request, 'form.html', {
            'form': form,
            'title': 'Edit Task',
        })
    else:
        # User is not authorized, sending him back to list
        return redirect('manager:list')

@login_required
def delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if task.user == request.user:
        # User is authorized to perform the action
        task.delete()
    
    # User is not authorized or deleted the task, sending him back to list
    return redirect('manager:list')

@login_required
def detail(request, pk):

    #User submit comment form
    if request.method == 'POST':
        form = NewCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.task_id = pk
            comment.author_id = request.user.id

            form.save()

            return redirect('manager:detail', pk=pk)
    #Loading detail page
    else:
        task = get_object_or_404(Task, pk=pk)
        comments = Comment.objects.filter(task=pk)

        if task.user == request.user or task.assignee == request.user:
            # User is authorized to perform the action
            form = NewCommentForm()

            return render(request, 'detail.html', {
                'task': task,
                'comments': comments,
                'form': form,
            })
        else:
            # User is not authorized, sending him back to list
            return redirect('manager:list')
        
@login_required
def mark_completed_task(request, pk):

    #Set the task to completed
    task = get_object_or_404(Task, id=pk)
    #Check and uncheck completed value
    if task.completed == False:
        task.completed = True
        task.completed_at = timezone.now()
    else:
        task.completed = False
        task.completed_at = None
    
    task.save()

    return redirect('manager:detail', pk=pk) 

@login_required
def configuration(request):

    if request.method == 'POST':

        if 'status_form' in request.POST:
            status_form = NewStatusForm(request.POST)

            if status_form.is_valid():
                status = status_form.save(commit=False)
                status.user_id = request.user.id

                status_form.save()

                return redirect('manager:configuration')
            
        elif 'priority_form' in request.POST:
            priority_form = NewPriorityForm(request.POST)

            if priority_form.is_valid():
                priority = priority_form.save(commit=False)
                priority.user_id = request.user.id

                priority.save()
                
                return redirect('manager:configuration')
            
        elif 'tag_form' in request.POST:
            tag_form = NewTagForm(request.POST)

            if tag_form.is_valid():
                tag = tag_form.save(commit=False)
                tag.user_id = request.user.id

                tag.save()
                
                return redirect('manager:configuration')
    
    else:
        statuses = Status.objects.filter(user_id=request.user.id)
        priorities = Priority.objects.filter(user_id=request.user.id)
        tags = Tag.objects.filter(user_id=request.user.id)

        status_form = NewStatusForm()
        priority_form = NewPriorityForm()
        tag_form = NewTagForm()

    return render(request, 'configuration.html', {
        'title': 'Configurations',
        'status_form': status_form,
        'priority_form': priority_form,
        'tag_form': tag_form,
        'statuses': statuses,
        'priorities': priorities,
        'tags': tags,
        'config_status_value': CONFIGURATION_STATUS_OBJECT,
        'config_priority_value': CONFIGURATION_PRIORITY_OBJECT,
        'config_tag_value': CONFIGURATION_TAG_OBJECT,
    })

@login_required
def configuration_delete(request, pk, cfg_obj):

    if cfg_obj == CONFIGURATION_STATUS_OBJECT:
        obj = Status
    elif cfg_obj == CONFIGURATION_PRIORITY_OBJECT:
        obj = Priority
    elif cfg_obj == CONFIGURATION_TAG_OBJECT:
        obj = Tag
    else:
        obj = None
    
    if obj is not None:
        object = get_object_or_404(obj, id=pk)
        
        if object.user == request.user:
            # User is authorized to perform the action
            try:
                object.delete()
            except ProtectedError:
                messages.error(request, f"Cannot delete {object.name} because it is used at a task.")

    # User is not authorized or deleted the object, sending him back to list
    return redirect('manager:configuration')

@login_required
def search(request):
    form = SearchForm(request.GET, user=request.user)
    query = None
    results = []

    if form.is_valid():
        #Retrieving the field values from the form
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        due_date = form.cleaned_data['due_date']
        assignee = form.cleaned_data['assignee']
        status = form.cleaned_data['status']
        priority = form.cleaned_data['priority']
        tag = [value for value in form.cleaned_data['tag'] if value != '']
        #Creating an empty query set
        results = Task.objects.none()

        #Building dinamic query based on the field values and setting the user_id
        query = Q()
        
        if title:
            query &= Q(title__icontains=title)
        if description:
            query &= Q(description__icontains=description)
        if due_date:
            query &= Q(due_date=due_date)
        if status:
            if status == '-1':
                query &= Q(completed=True)
            else:
                query &= Q(status=status)
                query &= Q(completed=False)
        if assignee:
            query &= Q(assignee=assignee)
        if priority:
            query &= Q(priority=priority)
        if tag:
            query &= Q(tags__in=tag)

        #Executing the query and retrieving the search results
        if query:
            query &= Q(user_id=request.user.id) | Q(assignee_id=request.user.id)
            results = Task.objects.filter(query)

    context = {
        'form': form,
        'results': results,
    }

    return render(request, 'search.html', context)


