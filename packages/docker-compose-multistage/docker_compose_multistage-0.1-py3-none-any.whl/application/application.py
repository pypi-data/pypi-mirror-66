import argparse

from application.config import Config
from application.parser import DockerComposeParser


class ArgumentParser:

    def __init__(self):
        self.result = None
        self.parser = argparse.ArgumentParser(description='Detect multiple target in dockerfile and process them.')
        self.parser.add_argument('--file', '-f', metavar='docker_compose_files', nargs='*', type=str,
                                 help='Path to docker-compose files', required=True)

    def parse(self, av):
        self.result = self.parser.parse_args(av[1:])

    def get_config(self):
        return Config(self.result)


class Application:

    def __init__(self, av):
        self.config = self._parse_config(av)

    @staticmethod
    def _parse_config(av):
        parser = ArgumentParser()
        parser.parse(av)
        return parser.get_config()

    def start(self):
        self._parse_services()
        self._process()

    def _parse_services(self):
        self._services = DockerComposeParser(self.config.get_docker_compose_files()).get_services()

    def _process(self):
        for service in self._services:
            service.pull_build_push_all()
