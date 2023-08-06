"""CLI handler."""
from tttimer.models.report import Report
import os


class CliHandler(object):
    """CLI handler."""

    def __init__(self):
        REPORTS_PATH = f'{os.getenv("HOME")}/.ttt_reports.json'
        print(REPORTS_PATH)
        self.report = Report(REPORTS_PATH)

    def start(self, task: str):
        """Start task."""
        self.report.start_task(task, 'None')

        print(f'Starting task {task}')

    def stop(self):
        """Stop task."""
        task = self.report.in_progress.task
        project = self.report.in_progress.project

        print(f'Stoping task {project}: {task}')
        self.report.stop()
