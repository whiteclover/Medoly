from medoly import kanon

import logging

LOGGER = logging.getLogger(__name__)


@kanon.hook("on_start_request")
def on_load(req_handler):
    LOGGER.debug("on load req_handler: %s", req_handler)


@kanon.error_page(404)
def not_found(req_handler, code, **kw):
    req_handler.render("404.html", page_title='Not Found')
