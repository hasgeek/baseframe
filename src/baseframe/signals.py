"""Baseframe signals."""

from blinker import Namespace

baseframe_signals = Namespace()

form_validation_error = baseframe_signals.signal('form-validation-error')
form_validation_success = baseframe_signals.signal('form-validation-success')
exception_catchall = baseframe_signals.signal('exception-catchall')
