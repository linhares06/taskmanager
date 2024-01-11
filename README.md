# Django Task Manager

A simple task manager built with Django framework and featuring Plotly graphs on the user's home page.

## Features

Task creation and management. <br/>
Due dates and priorities. <br/>
Assign tasks to other users. <br/>
Comment and collaborate on tasks. <br/>
Track task progress and completion. <br/>
Viewing graphs: <br/>
**Completed Task Per Day:** Visual representation of completed tasks per day over the last 30 days. <br/>
**Task by Status:** Visualize the distribution of tasks based on their status (e.g., To Do, In Progress, Completed). <br/>
**Task Duration:** Duration analysis of completed tasks, helping to identify trends. <br/>
**Assignee Productivity:** Productivity analysis based on tasks assigned to other users. <br/>

## Prerequisites

- Python 3.11.5
- Django 4.2.7

## Running

1. Clone repository.
2. Install dependencies: pip install requirements.txt
3. Apply migrations: python manage.py migrate
4. Create a superuser account: python manage.py createsuperuser
5. Start server by running: python manage.py runserver
6. Access the task manager at http://localhost:8000.
