# -*- coding: utf-8 -*-
# copyright 2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-subprocess entity's classes"""

import os
import json
import signal
from subprocess import PIPE, Popen, list2cmdline

from cubicweb import ValidationError, Binary, _
from cubicweb.entities import AnyEntity

from cubicweb_subprocess.error import ProcessNotRunning
from cubicweb_subprocess.utils import communicate


def kill(pid):
    if os.name == 'posix':
        # no windows support for this before python 2.7 ...
        os.kill(pid, signal.SIGTERM)
    else:
        proc = Popen(['taskkill', '/f', '/t', '/pid', '%s' % pid])
        proc.wait()


class Subprocess(AnyEntity):
    __regid__ = 'Subprocess'
    envencoding = 'utf-8'

    def dc_title(self):
        try:
            return u' '.join(json.loads(self.cmdline))
        except (ValueError, TypeError):
            return self.cmdline

    @property
    def finished(self):
        '''Return True is the process has been run and finished.'''
        return not list(
            self.cw_adapt_to('IWorkflowable').possible_transitions()
        )

    def _create_output_file(self, name):
        return self._cw.create_entity(
            'File',
            data=Binary(),
            data_format=u'text/plain',
            data_name=name,
            output_of=self,
        )

    def _environ(self):
        env = os.environ.copy()
        env.update(json.loads(self.env) if self.env else {})
        return dict(
            (k.encode(self.envencoding) if isinstance(k, str) else k,
             v.encode(self.envencoding) if isinstance(v, str) else v)
            for k, v in env.items()
        )

    def _launch(self):
        """Launch a subprocess defined.

        The pid is stored in the db as soon as the subprocess is created,
        so that it can be used right away (for killing or status checking).

        Once terminated, the workflow transition is fired according to the
        return code of the subprocess.
        """
        cmd_args = json.loads(self.cmdline)
        proc = Popen(cmd_args, cwd=self.cwd,
                     env=self._environ(),
                     stdout=PIPE, stderr=PIPE)
        outputs = {'stdout': self._create_output_file(u'stdout'),
                   'stderr': self._create_output_file(u'stderr')}
        self.cw_set(pid=proc.pid)
        self.info('started subprocess with pid %d (cmdline: %s)',
                  proc.pid, list2cmdline(cmd_args))
        self._cw.commit()

        for outname, content in communicate(proc):
            self.debug('Appending %s bytes to %s (stream %s)',
                       len(content), outputs[outname].eid, outname)
            outputs[outname].data.write(content)
            outputs[outname].cw_set(data=outputs[outname].data)
            outputs[outname].data.seek(0, 2)  # go to the end of stream
            self._cw.commit()

        return proc.wait()

    def _finalize(self, return_code, trname):
        """Save subprocess metadata into the database"""
        adapted = self.cw_adapt_to('IWorkflowable')
        if adapted.state == 'in progress':   # can be in other state if it
            adapted.fire_transition(trname)  # was killed.
        self.cw_set(return_code=return_code)
        self._cw.commit()

    def _start(self):
        """Process the subprocess"""
        return_code = self._launch()
        trname = 'complete' if return_code == 0 else 'abort'
        self._finalize(return_code, trname)

    @property
    def stderr(self):
        return self.get_output(u'stderr')

    @property
    def stdout(self):
        return self.get_output(u'stdout')

    def get_output(self, name):
        data = self._cw.find('File', output_of=self, data_name=name).one().data
        if data is not None:
            return data.getvalue()

    def start(self):
        """start the subprocess."""
        assert self.cw_adapt_to('IWorkflowable').state == 'in progress'

        def _launch():
            with self._cw.repo.internal_cnx() as cnx:  # dedicated cnx in thread
                cnx.entity_from_eid(self.eid)._start()
        self.info('launching subprocess #%d', self.eid)
        self._cw.repo.threaded_task(_launch)

    def synchronousstart(self):
        """start the subprocess."""
        cnx = self._cw
        wfadapter = self.cw_adapt_to('IWorkflowable')
        assert wfadapter.state == 'initialized'
        with cnx.allow_all_hooks_but('subprocess.workflow'):
            # this ^^ must be inhibited if we want control
            wfadapter.fire_transition('start', u'started synchronous subprocess')
            cnx.commit()
        self.cw_clear_all_caches()
        self._start()
        return self.return_code

    def _kill(self):
        """kill the subprocess if it's running.
        """
        pid = self.pid
        if pid is None:
            raise ProcessNotRunning('The process is not started')
        kill(pid)

    def kill(self):
        """kill the subprocess if it is running."""
        if not self.cw_adapt_to('IWorkflowable').state == 'in progress':
            raise ValidationError(self.eid, {
                None: _('You must use the workflow to start the subprocess')})
        self._kill()
