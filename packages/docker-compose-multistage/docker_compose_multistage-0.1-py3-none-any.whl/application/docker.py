from application.docker_cli import Docker
from application.logger import Logger


class BuildContext:

    def __init__(self, context, dockerfile):
        self._context = context
        self._dockerfile = dockerfile

    def get_context(self):
        return self._context

    def get_dockerfile(self):
        return self._dockerfile

    def get_dockerfile_full_path(self):
        return '{}/{}'.format(self.get_context(), self.get_dockerfile())


class Image:

    def __init__(self, repository):
        self._repository = repository

    def get_path(self, tag='latest'):
        return '{}:{}'.format(self._repository, tag)


class Service:

    def __init__(self, name, image, build_context, stages):
        """
        :type image: Image
        :type build_context: BuildContext
        :type stages: StageCollection
        """
        self._name = name
        self._image = image
        self._build_context = build_context
        self._stages = stages

    def get_stage(self):
        return self._stages

    def get_build_context(self):
        return self._stages

    def get_stages(self):
        return self._stages

    def pull_build_push_all(self):
        Logger.prefix('[{}] '.format(self._name))
        Logger.log('Start caching')
        for stage in self._stages:
            self._pull_build_push_stage(stage)

    def _pull_build_push_stage(self, stage):
        Logger.prefix('[{}][{}] '.format(self._name, stage))
        Logger.log('Start caching')
        self._pull(stage)
        self._build(stage)
        self._push(stage)

    def _pull(self, stage):
        path = self._image.get_path(tag=stage)
        Logger.log('Pulling from {}'.format(path))
        Docker().pull(path)

    def _build(self, stage):
        path = self._image.get_path(tag=stage)
        Logger.log("Building from {}".format(self._build_context.get_dockerfile_full_path()))
        Docker().build(self._build_context.get_context(), self._build_context.get_dockerfile(), stage, path, path)

    def _push(self, stage):
        path = self._image.get_path(tag=stage)
        Logger.log('Pushing to {}'.format(path))
        Docker().push(path)
