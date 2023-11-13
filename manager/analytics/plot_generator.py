import plotly.graph_objects as go
from plotly import offline

class PlotGenerator:

    def generate_task_per_day(self, dates, counts):

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

        fig = go.Figure(data=go.Pie(labels=status, values=counts))

        chart_html = offline.plot(fig, auto_open=False, output_type='div')

        return chart_html
    
    def generate_task_duration(self, task_durations, task_names):

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