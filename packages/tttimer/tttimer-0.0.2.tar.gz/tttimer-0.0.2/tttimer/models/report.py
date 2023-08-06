"""Report model."""

import json

from tttimer.models.time_frame import TimeFrame


class Report(object):
    in_progress: TimeFrame
    timeframe_list: list

    def __init__(self, filePath: str):
        self._filePath = filePath
        self.timeframe_list = self._load_list_from_file()
        self.in_progress = self._find_in_progress()

    def start_task(self, name: str, project: str):
        newTimeframe = TimeFrame(name, project)
        self.timeframe_list.append(newTimeframe)
        self.in_progress = self._find_in_progress()
        self._save()

    def stop(self):
        self.in_progress.stop()
        self._save()

    def _load_list_from_file(self):
        try:
            with open(self._filePath) as file:
                return [
                    TimeFrame.fromJson(tf) for tf in json.loads(file.read())
                ]
        except FileNotFoundError:
            return []
        except json.decoder.JSONDecodeError:
            return []

    def _save(self):
        with open(self._filePath, 'w+') as file:
            file.write(json.dumps([
                tf.toJson() for tf in self.timeframe_list
            ]))

    def _find_in_progress(self):
        for tf in self.timeframe_list:
            if tf.is_in_progress():
                return tf
        return None
