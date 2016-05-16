import logging


def log_config(tag, debug=False):
    """Be used for confguration log level and format

    Example::

        log_config('log_test', debug=True)
        logger = logging.getLogger('utils')
        logger.debug('test debug')
        logger.debug('test debug')

    """
    logfmt = tag + '[%%(process)d]: [%%(levelname)s] %s%%(message)s' % '%(name)s - '

    def config(x):
        """Config log message level and format"""
        logging.basicConfig(level=x, format='[%(asctime)s] ' + logfmt, datefmt='%Y%m%d %H:%M:%S')

    if debug:
        config(logging.DEBUG)
    else:
        config(logging.INFO)
