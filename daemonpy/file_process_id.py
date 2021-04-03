# -*- coding: UTF-8 -*-

'''
 Module
     file_process_id.py
 Copyright
     Copyright (C) 2020 Vladimir Roncevic <elektron.ronca@gmail.com>
     daemonpy is free software: you can redistribute it and/or modify it
     under the terms of the GNU General Public License as published by the
     Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.
     daemonpy is distributed in the hope that it will be useful, but
     WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
     See the GNU General Public License for more details.
     You should have received a copy of the GNU General Public License along
     with this program. If not, see <http://www.gnu.org/licenses/>.
 Info
     Defined class FileProcessId with attribute(s) and method(s).
     Created API for file process id context management.
'''

from sys import exit
from os.path import exists

try:
    from ats_utilities.checker import ATSChecker
    from ats_utilities.console_io.error import error_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_bad_call_error import ATSBadCallError
    from ats_utilities.exceptions.ats_parameter_error import ATSParameterError
except ImportError as ats_error_message:
    MESSAGE = '\n{0}\n{1}\n'.format(__file__, ats_error_message)
    exit(MESSAGE)  # Force close python ATS ##############################

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright 2020, https://vroncevic.github.io/daemonpy'
__credits__ = ['Vladimir Roncevic']
__license__ = 'https://github.com/vroncevic/daemonpy/blob/master/LICENSE'
__version__ = '1.5.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FileProcessId(object):
    '''
        Defined class FileProcessId with attribute(s) and method(s).
        Created API for file descriptor context management.
        It defines:

            :attributes:
                | __slots__ - Setting class slots.
                | VERBOSE - Console text indicator for current process-phase.
                | __MODE - Supported modes for process id file.
                | __file_process_id_path - PID file path.
                | __file_process_id_mode - PID file mode.
                | __file_process_id - PID file object.
            :methods:
                | __init__ - Initial constructor.
                | __enter__ - Open PID file.
                | __exit__ - Close PID file.
                | __str__ - Dunder method for object FileDescriptor.
    '''

    __slots__ = (
        'VERBOSE', '__MODE', '__file_process_id_path',
        '__file_process_id_mode', '__file_process_id'
    )
    VERBOSE = 'DAEMONPY::FILE_PROCESS_ID'
    __MODE = ['w+', 'r']

    def __init__(self, file_process_id_path, file_process_id_mode):
        '''
            Initial constructor.

            :param file_process_id_path: File process id path.
            :type file_process_id_path: <str>
            :param file_process_id_mode: File process id mode.
            :type file_process_id_mode: <str>
            :exceptions: ATSTypeError | ATSBadCallError
        '''
        checker, error, status = ATSChecker(), None, False
        error, status = checker.check_params([
            ('str:file_process_id_path', file_process_id_path),
            ('str:file_process_id_mode', file_process_id_mode)
        ])
        if status == ATSChecker.TYPE_ERROR:
            raise ATSTypeError(error)
        if status == ATSChecker.VALUE_ERROR:
            raise ATSBadCallError(error)
        if file_process_id_mode in FileProcessId.__MODE:
            self.__file_process_id_path = file_process_id_path
            self.__file_process_id_mode = file_process_id_mode
            self.__file_process_id = None
        else:
            error = 'PID file mode can be <w+ | r>'
            error_message(FileProcessId.VERBOSE, error)

    def __enter__(self):
        '''
            Open PID file.

            :return: File device object | None.
            :rtype: <file> | <NoneType>
            :exceptions: ATSParameterError
        '''
        error = None
        if self.__file_process_id_mode == FileProcessId.__MODE[1]:
            if not exists(self.__file_process_id_path):
                error = 'check PID file path'
                raise ATSParameterError(error)
            else:
                pass
        elif self.__file_process_id_mode == FileProcessId.__MODE[0]:
            pass
        else:
            error = 'check PID file mode'
            raise ATSParameterError(error)
        self.__file_process_id = open(
            self.__file_process_id_path, self.__file_process_id_mode
        )
        return self.__file_process_id

    def __exit__(self, *args):
        '''
            Close PID file.

            :exceptions: None
        '''
        try:
            self.__file_process_id.close()
        except AttributeError:
            pass

    def __str__(self):
        '''
            Dunder method for FileProcessId.

            :return: Object in a human-readable format.
            :rtype: <str>
            :exceptions: None
        '''
        return '{0} ({1}, {2}, {3})'.format(
            self.__class__.__name__, self.__file_process_id_path,
            self.__file_process_id_mode, self.__file_process_id
        )
