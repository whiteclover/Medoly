import logging

def log_config(tag, debug=False):
    """"
    be used for confguration log level and format
    >>> log_config('log_test', debug=True)
    >>> logger = logging.getLogger('utils')
    >>> logger.debug('test debug')
    >>> logger.info('test info')

    """
    logfmt = tag + \
        '[%%(levelname)s] %s%%(message)s' % '%(name)s - '
    config = lambda x: logging.basicConfig(
        level=x, format='[%(asctime)s] ' + logfmt, datefmt="%Y%m%d %H:%M:%S")
    if debug:
        config(logging.DEBUG)
    else:
        config(logging.INFO)
