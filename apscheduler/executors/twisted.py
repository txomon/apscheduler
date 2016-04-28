from __future__ import absolute_import

from apscheduler.executors.base import BaseExecutor, job_runtime


class TwistedExecutor(BaseExecutor):
    """
    Runs jobs in the reactor's thread pool.

    Plugin alias: ``twisted``
    """

    def start(self, scheduler, alias):
        super(TwistedExecutor, self).start(scheduler, alias)
        self._reactor = scheduler._reactor

    def _do_submit_job(self, job, run_times):
        def callback(success, result):
            if success:
                self._run_job_success(job.id, result)
            else:
                self._run_job_error(job.id, result.value, result.tb)

        self._reactor.getThreadPool() \
            .callInThreadWithCallback(callback, job_runtime, job, run_times, self._logger.name)
