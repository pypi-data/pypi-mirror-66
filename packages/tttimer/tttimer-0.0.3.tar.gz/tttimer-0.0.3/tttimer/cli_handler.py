"""CLI handler."""
from tttimer.models.report import Report
import os


class CliHandler(object):
    """CLI handler."""

    def __init__(self):
        REPORTS_PATH = f'{os.getenv("HOME")}/.ttt_reports.json'
        self.report = Report(REPORTS_PATH)

    def start(self, task: str):
        """Start task."""
        if self.report.in_progress:
            print(f"Ops, task '{self.report.in_progress.task}' in progress.")
            print('You must stop it first.')
            return

        self.report.start_task(task, 'None')
        print(f'Starting task {task}')

    def stop(self):
        """Stop task."""
        task = self.report.in_progress.task
        project = self.report.in_progress.project

        print(f'Stoping task {project}: {task}')
        self.report.stop()
