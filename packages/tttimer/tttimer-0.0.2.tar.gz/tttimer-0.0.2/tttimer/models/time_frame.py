"""TimeFrame model."""

import time


class TimeFrame(object):
    def __init__(
        self,
        task: str,
        project: str
    ):
        self.task = task
        self.project = project
        self.start_time = time.time()
        self.end_time = None

    def stop(self):
        self.end_time = time.time()

    def is_in_progress(self):
        return not bool(self.end_time)

    def toJson(self):
        return {
          'task': self.task,
          'project': self.project,
          'start_time': self.start_time,
          'end_time': self.end_time,
        }

    @staticmethod
    def fromJson(jsonObject: dict):
        newTimeframe = TimeFrame(jsonObject['task'], jsonObject['project'])
        newTimeframe.end_time = jsonObject.get('end_time')
        newTimeframe.start_time = jsonObject['start_time']

        return newTimeframe
