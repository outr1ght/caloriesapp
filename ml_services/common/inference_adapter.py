from abc import ABC, abstractmethod


class InferenceAdapter(ABC):
    @abstractmethod
    def predict(self, payload: dict) -> dict:
        raise NotImplementedError
