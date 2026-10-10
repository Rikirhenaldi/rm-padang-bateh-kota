from abc import ABC, abstractmethod


class StorageError(Exception):
    pass


class StorageBackend(ABC):
    @abstractmethod
    def load_json(self, name):
        raise NotImplementedError

    @abstractmethod
    def save_json(self, name, value, message):
        raise NotImplementedError

    @abstractmethod
    def save_image(self, path, content, message):
        raise NotImplementedError

    @abstractmethod
    def delete_image(self, path, message):
        raise NotImplementedError

    @abstractmethod
    def read_image(self, path):
        raise NotImplementedError

    def invalidate(self):
        return None
