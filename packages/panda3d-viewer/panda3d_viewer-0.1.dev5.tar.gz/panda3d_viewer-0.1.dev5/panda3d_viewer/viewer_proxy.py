"""This module contains a viewer application process proxy."""

import multiprocessing as mp

from .viewer_errors import ViewerClosedError

__all__ = ('ViewerAppProxy')


class ViewerAppProxy(mp.Process):
    """A viewer application process proxy.

    Run a viewer application in a separate process to
    use it in an asynchronous way.
    """

    def __init__(self, *args, **kwargs):
        """Start an application in a sub-process."""
        mp.Process.__init__(self)
        self._args = args
        self._kwargs = kwargs
        self._queue = mp.Queue()
        self.daemon = True
        self.start()

    def __getattr__(self, name):
        """Get attribute hook.

        Intercepts method calls and redirects to the sub-process.

        Arguments:
            name {str} -- attribute name

        Raises:
            ViewerClosedError: if the viewer application is not alive

        Returns:
            callable -- an application method wrapper
        """
        def _send(*args, **kwargs):
            if not self.is_alive():
                raise ViewerClosedError('Viewer process is not alive')
            self._queue.put((name, args, kwargs))

        return _send

    def run(self):
        """Run the application in a sub-process."""
        # import here to prevent Panda3D from loading in the host process
        from .viewer_app import ViewerApp    # pylint: disable=import-outside-toplevel

        app = ViewerApp(*self._args, **self._kwargs)

        def _execute(task):
            while not self._queue.empty():
                name, args, kwargs = self._queue.get_nowait()
                if name == 'step':
                    # let the manager to execute other tasks
                    break
                getattr(app, name)(*args, **kwargs)
            return task.cont

        app.taskMgr.add(_execute, "Exec commands from the host process", -50)
        app.run()
