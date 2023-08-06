#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# errors.py: functions related to error handling
import os
import sys
import logging
import traceback

from xtlib import utils
from .console import console

logger = logging.getLogger(__name__)

def exception_msg(ex):
    parts = str(ex).split("\n")
    return parts[0]

def user_exit(msg):
    raise Exception(msg)

def early_exit_without_error(msg=None):
    '''
    This is not an error; just information that request terminated early.
    '''
    if msg:
        console.print(msg)
    sys.exit(0)

def syntax_error_exit():
    # use "os._exit" to prevent exception from being thrown
    os._exit(1)

def report_exception(ex, operation=None):
    #console.print("Error: " + exception_msg(ex))
    raise ex

def process_exception(ex_type, ex_value, ex_traceback, exit_app=True):
    msg = str(ex_value)

    #if utils.show_stack_trace:
    # if we did not raise this exception, we should show a stack trace
    if not issubclass(ex_type, XTBaseException):
        if exit_app:
            raise ex_value
        traceback.print_exception(ex_type, ex_value, ex_traceback)
    else:
        console.print()
        console.print("Exception: " + msg)
       
        # for debugging print stack track
        traceback.print_exc()

    # bug workaround
    #if isinstance(ex, SyntaxError):
    if msg.startswith("Syntax error"):
        # show syntax/args for command
        from .qfe import current_dispatcher
        current_dispatcher.show_current_command_syntax()

    # use "os._exit" to prevent a 2nd exception from being thrown
    os._exit(1)

class XTBaseException(Exception): pass

class UserError(XTBaseException): pass
class InternalError(XTBaseException): pass
class SyntaxError(XTBaseException): pass
class ComboError(XTBaseException): pass
class EnvError(XTBaseException): pass
class ConfigError(XTBaseException): pass
class StoreError(XTBaseException): pass
class ServiceError(XTBaseException): pass
class GeneralError(XTBaseException): pass
class APIError(XTBaseException): pass
class CredentialsError(XTBaseException): pass

class ControllerNotYetRunning(XTBaseException): pass

# following functions handle the different classes of errors

def internal_error(msg):
    raise InternalError(msg)

def syntax_error(msg):    
    raise SyntaxError(msg)

def creds_error(msg):    
    raise CredentialsError(msg)

def combo_error(msg):    
    raise ComboError(msg)

def env_error(msg):    
    raise EnvError(msg)

def config_error(msg):    
    raise ConfigError(msg)

def store_error(msg):    
    raise StoreError(msg)

def service_error(msg):    
    raise ServiceError(msg)

def general_error(msg):
    raise GeneralError(msg)

def api_error(msg):
    raise APIError(msg)

def controller_not_yet_running(msg):
    raise ControllerNotYetRunning(msg)

def argument_error(arg_type, token):
    if token.startswith("-"):
        token2 = "-" + token
    else:
        token2 = "--" + token
    #syntax_error("expected {}, but found '{}'.  Did you mean '{}'?".format(arg_type, token, token2))    
    syntax_error("unrecognized argument: {}?".format(token))
