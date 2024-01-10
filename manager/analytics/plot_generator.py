import plotly.graph_objects as go
from plotly import offline

class PlotGenerator:
    """
    A class for generating various types of plots using Plotly.

    Attributes:
    - None

    Methods:
    - generate_task_per_day(dates, counts): Generate a line chart representing tasks per day.
    - generate_task_by_status(status, counts): Generate a pie chart representing tasks by status.
    - generate_task_duration(task_durations, task_names): Generate a horizontal bar chart representing task durations.
    - generate_assignee_productivity(assignees, completed_tasks): Generate grouped bar and pie charts
      representing assignee productivity based on completed tasks.
    """
    def generate_task_per_day(self, dates, counts):
        """
        Generate a line chart representing tasks per day.

        Args:
        - dates (list): List of dates.
        - counts (list): List of corresponding task counts.

        Returns:
        - chart_html (str): HTML string containing the generated chart.
        """
        data = go.Scatter(
            x=dates,
            y=counts,
            mode='lines+markers',
        )

        layout = go.Layout(
            xaxis=dict(title='Date'),
            yaxis=dict(title='Task Count')
        )

        fig = go.Figure(data=[data], layout=layout)
        fig.update_layout(yaxis=dict(tickformat='.0f', tick0=0, dtick=1), xaxis=dict(tickformat="%Y-%m-%d"))

        chart_html = offline.plot(fig, auto_open=False, output_type='div')

        return chart_html
    
    def generate_task_by_status(self, status, counts):
        """
        Generate a pie chart representing tasks by status.

        Args:
        - status (list): List of status labels.
        - counts (list): List of corresponding task counts.

        Returns:
        - chart_html (str): HTML string containing the generated chart.
        """
        fig = go.Figure(data=go.Pie(labels=status, values=counts))

        chart_html = offline.plot(fig, auto_open=False, output_type='div')

        return chart_html
    
    def generate_task_duration(self, task_durations, task_names):
        """
        Generate a horizontal bar chart representing task durations.

        Args:
        - task_durations (list): List of task durations.
        - task_names (list): List of corresponding task names.

        Returns:
        - chart_html (str): HTML string containing the generated chart.
        """
        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=task_names,
            x=task_durations,
            orientation='h',
            marker=dict(color='blue'),
        ))

        fig.update_layout(
            xaxis_title='Duration (Days)',
            yaxis_title='Task',
        )

        chart_html = offline.plot(fig, auto_open=False, output_type='div')

        return chart_html
    
    def generate_assignee_productivity(self, assignees, completed_tasks):
        """
        Generate grouped bar and pie charts representing assignee productivity based on completed tasks.

        Args:
        - assignees (list): List of assignees.
        - completed_tasks (list): List of completed task counts for each assignee.

        Returns:
        - bar_chart_html (str): HTML string containing the generated grouped bar chart.
        - pie_chart_html (str): HTML string containing the generated pie chart.
        """
        bar_fig = go.Figure(data=[
            go.Bar(name='Completed Tasks', text=completed_tasks, x=assignees, y=completed_tasks),
        ])
        bar_fig.update_layout(
            xaxis_title='Assignee',
            yaxis_title='Count',
            barmode='group'
        )
        bar_chart_html = offline.plot(bar_fig, auto_open=False, output_type='div')

        pie_fig = go.Figure(data=go.Pie(labels=assignees, values=completed_tasks))
        pie_chart_html = offline.plot(pie_fig, auto_open=False, output_type='div')

        return bar_chart_html, pie_chart_html