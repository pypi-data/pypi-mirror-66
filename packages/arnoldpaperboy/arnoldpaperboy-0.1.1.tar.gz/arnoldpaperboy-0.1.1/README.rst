Arnold the Paperboy
===================

Delivers the Daily Slab. As a python package, it also facilitates
logging from python in kubernetes to stackdriver.

Arnoldpaperboy is developed by Satelligence ("S11") to aid proper logging to Stackdriver from python
processes running in Kubernetes. With as little influence on existing code as possible.

TL;DR:
------

Assume there is existing code which uses
::

    logger = logging.getLogger(__name__)

everywhere on top of the python files, and uses this `logger` object throught the rest of the code
to do logging calls. To enable Stackdriver enhanced logging and profiling, just add
::

    from arnoldpaperboy.helpers import autolog

in the imports section, and annotate every function or method from which you want to have better
Stackdriver logging, or which you'd want to have profile information in Stackdriver logs with the
::

    @autolog(level=logging.LEVEL)

and suddenly

* every ``logger.info|warning|debug|...`` call will send a properly formatted log message to
  Stackdriver, with a k8s_container resource with all labels filled, with information on from which
  file, function and line the logger was called, and with additional items in the ``labels`` section
  for every arg or kwarg the decorated function was called with;
* a log message will be sent to Stackdriver right before calling the decorated function ("Starting
  <package.module.function>");
* a log message will be sent to Stackdriver when the decorated function is finished, with additional
  temporal profiling information (the function call duration): "Finished <package.module.function>
  in h:mm:ss".


How does it work?
-----------------

Currently, the package contains 3 parts, which, when tied together, enable (Stackdriver) logging and
profiling for existing code by simply adding an import and a decorator call.


StackdriverLoggingHandler
~~~~~~~~~~~~~~~~~~~~~~~~~

StackdriverLoggingHandler class in logging_handlers.py: this is a customized logging handler which
derives from the google.cloud.logging.handlers.CloudLoggingHandler. The StackdriverLoggingHandler
adds a properly formatted and filled Stackdriver `resource` object, adds some extra information to
the Stackdriver ``labels``, and adds any extra attributes from the python LogRecord object to
``labels``. When using the StackdriverLoggingHandler as-is, you would add these extra attributes to
the LogRecord by specifying an ``extra={'somekey':'somevalue', ...:...}`` to a logging statement. Due
to how python logging works, these ``extra`` attributes automatically end up as attributes on the
LogRecord instance.


AnnotatedLogger
~~~~~~~~~~~~~~~

AnnotatedLogger in helpers.py is a context manager (so it can be used in a ``with`` statement) which
magically picks up an earlier defined logger instance (by name, default='logger'), and for the
new context replaces that with a (slightly enhanced) LoggerAdapter instance. This is very useful if
there already is code with ``logger = logging.getLogger(__name__)`` on top of the files, and the use
of this ``logger`` throughout the code. Without the trick to get a logger from a global scope, the new
annotated logger cannot have the same name as the existing (global) logger.
The new annotated logger is annotated with all the kwargs it is instantiated with, and so it
eliminates the ugly need for an ``extra={...}`` keyword. Instead, within the new context, the existing
logger can be used as is, and every keyword that was specified in the ``AnnotatedLogger(...)`` call
will be added to every logging call.


autolog
~~~~~~~

Autolog is a decorator function which replaces an existing global logger with a new annotated logger
while the decorated function is being called. The caller's arguments and keyword arguments are
automatically added to the annotated logger (with an extra "arg\_" prefix). Profiling is enabled
through the ``log_before`` and ``log_after`` keywords, which when True will automatically send a log
message before and after calling the decorated function, the last one enriched with profiling
information (duration in seconds and formatted as human readable time).


Usage example
-------------

Use case: existing code base, running on k8s, using Django framework. Wish: proper logging to
Stackdriver while keeping the existing code base intact as much as possible.

First, enable proper formatted logging to Stackdriver. Configure django logging by extending the
existing django logconfig like this::

    from google.cloud.logging import Client
    STACKDRIVER_CLIENT = Client(project=GOOGLE_PROJECT_ID)
    LOG_HANDLERS = ['stackdriver']

    LOG_HANDLER_CONFIG['stackdriver'] = {
        'class': 'arnoldpaperboy.logging_handlers.StackdriverLoggingHandler',
        'client': STACKDRIVER_CLIENT,
        'tier': 'your-tier-name',
        'app': 'your-app-name',
    }

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': LOG_HANDLER_CONFIG,
        'loggers': {
            # root logger
            '': {
                'level': LOGLEVEL_ROOT,
                'name': TIER,
                'handlers': LOG_HANDLERS,
            },
        },
    })

then to enable enhanced logging to Stackdriver, Just add

::

    from arnoldpaperboy.helpers import autolog

and decorate each function or method from where the enhanced logging to stackdriver should be
enabled with the autolog decorator::

    @autolog(level=...)

Magic!
