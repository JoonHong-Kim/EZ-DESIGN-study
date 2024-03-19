import threading

import pandas as pd


class Metrics:
    _instance = None
    _lock = threading.Lock()

    _metrics = {}

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        try:
            self._metrics = pd.read_csv("metrics.csv", index_col=0).T.to_dict()
        except FileNotFoundError:
            self._metrics = {}

    @property
    def metrics(self):
        return self._metrics

    def set(self, key, value):
        self._metrics[key] = value

    def save(self):
        df = pd.DataFrame(self._metrics).T
        df.to_csv("metrics.csv")
