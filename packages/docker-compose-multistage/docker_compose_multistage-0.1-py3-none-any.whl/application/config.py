from application.logger import Logger


class Config:
    _instance = None

    def __init__(self, config):
        self.config = config
        Logger()
        Config._instance = self

    @staticmethod
    def instance():
        return Config._instance

    def get_docker_compose_files(self):
        return self.config.file

