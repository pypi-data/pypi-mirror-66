import functools
import logging
import os

if os.getenv("KRON_INSPECT_DRIVER_QUERIES"):
    LOGGING_INVISIBLE = logging.DEBUG
else:
    LOGGING_INVISIBLE = 0

log = logging.getLogger("kron.driver")
log.invisible = functools.partial(log.log, LOGGING_INVISIBLE)
