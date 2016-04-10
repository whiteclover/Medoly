import os

from choco.lookup import TemplateLookup
from tornado.template import Loader


class ChocoTemplateLoader(Loader):
    def __init__(self, directories, ui_container=None, module_directory=None, filesystem_checks=False,  **kwargs):
        super(ChocoTemplateLoader, self).__init__(directories[0], **kwargs)
        
        self._lookup = TemplateLookup(directories=directories, 
                                    ui_container=ui_container,
                                    filesystem_checks=filesystem_checks,
                                    module_directory=module_directory,
                                    input_encoding='utf-8',
                                    output_encoding='utf-8',
                                    default_filters=['decode.utf8'])

    def _create_template(self, name):
        template = self._lookup.get_template(name)
        template.generate = template.render

        return template
