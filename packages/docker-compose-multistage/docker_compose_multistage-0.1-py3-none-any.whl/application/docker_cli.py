import subprocess

from application.logger import Logger


class Docker:

    def pull(self, image):
        self._docker('pull -q', image)

    def build(self, context, dockerfile, stage, tag, cache_from):
        self._docker('build', context, file=context + '/' + dockerfile, target=stage, tag=tag, cache_from=cache_from)

    def push(self, image):
        self._docker('push', image)

    def _docker(self, *args, **kwargs):
        command = ['docker', *args]
        for key in kwargs:
            command.extend(['--' + key.replace('_', '-'), kwargs[key]])
        self._command(command)

    @staticmethod
    def _command(args):
        process = subprocess.Popen(' '.join(args), shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        running = True
        while running:
            [stdout, stderr] = process.communicate()
            if stdout:
                Logger.log(stdout.decode('ascii'))
            if stderr:
                Logger.err(stderr.decode('ascii'))
            running = process.poll() is None
