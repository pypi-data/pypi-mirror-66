"""CLI handler."""
import os

from tttimer.models.report import Report
from PyInquirer import prompt


class CliHandler(object):
    """CLI handler."""

    def __init__(self):
        REPORTS_PATH = f'{os.getenv("HOME")}/.ttt_reports.json'
        self.report = Report(REPORTS_PATH)

    def start(self, path: str = os.getenv("WORK")):
        """Start task."""
        project_path = f'{os.getenv("HOME")}/dev'
        if path:
            project_path = path

        if self.report.in_progress:
            print(f"Ops, task '{self.report.in_progress.task}' in progress.")
            print('You must stop it first.')
            return

        answer = prompt([
            {
                'type': 'input',
                'name': 'task',
                'message': 'Task name:',
            },
            {
                'type': 'list',
                'name': 'project',
                'message': 'Select a project:',
                'choices': os.listdir(project_path)
            },
        ])

        self.report.start_task(answer['task'], answer['project'])
        print(f'Starting task "{answer["task"]}" in "{answer["project"]}"')

    def stop(self):
        """Stop task."""
        if not self.report.in_progress:
            return print("You are not working.")

        task = self.report.in_progress.task
        project = self.report.in_progress.project

        print(f'Stoping task "{project}: {task}"')
        self.report.stop()

    def status(self):
        """Stop task."""
        if self.report.in_progress:
            task = self.report.in_progress.task
            project = self.report.in_progress.project

            return print(f'> Working in task "{project}: {task}".')

        print('Not loggin work now.')
