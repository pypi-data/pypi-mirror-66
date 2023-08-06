import subprocess

from yaml import load, Loader

from application.docker import BuildContext, Image, Service


class StageParser:

    def __init__(self, build_context):
        """
        :type build_context BuildContext
        """
        self._stages = []
        self._build_context = build_context

    def parse_stages(self):
        self._stages = []
        self._parse_file(open(self._build_context.get_dockerfile_full_path()))
        stages = self._stages
        self._stages = None
        return stages

    def _parse_file(self, file):
        for line in file:
            self._parse_line(line.strip())

    def _parse_line(self, line):
        if line.startswith('FROM'):
            self._add_target_name(line)

    def _add_target_name(self, line):
        args = line.split(' ')
        if len(args) == 4:
            self._stages.append(args[3])


class ServiceParser:

    def __init__(self, name, service):
        self._name = name
        self._service = service
        self._build_context = None

    def parse(self):
        self._build_context = self._get_build_context()

        return Service(
            name=self._name,
            image=self._get_image(),
            build_context=self._build_context,
            stages=self._get_stages()
        )

    def _get_image(self):
        return Image(repository=self._service.get('image'))

    def _get_build_context(self):
        return BuildContext(
            context=self._service.get('build').get('context'),
            dockerfile=self._service.get('build').get('dockerfile'),
        )

    def _get_stages(self):
        return StageParser(self._build_context).parse_stages()


class DockerComposeParser:
    """
    :type config Dict[Hashable, Dict[Hashable, Dict]]
    """
    config = None

    def __init__(self, docker_compose_files):
        self._docker_compose_files = docker_compose_files
        self._service = None

    def get_services(self):
        self._service = []
        self.config = self._get_docker_compose_config()
        self._parse_pushable_services()
        return self._service

    def _get_docker_compose_config(self):
        command = ['docker-compose']
        for filename in self._docker_compose_files:
            command.extend(['-f', filename])
        command.append('config')
        output = subprocess.check_output(command)
        return load(output, Loader)

    def _parse_pushable_services(self):
        for [name, service] in self.config.get('services').items():
            self._parse_service(name, service)

    def _parse_service(self, name, service):
        if 'image' in service and 'build' in service:
            self._service.append(
                ServiceParser(name, service).parse()
            )
