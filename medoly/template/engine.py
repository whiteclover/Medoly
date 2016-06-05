#!/usr/bin/env python
#
# Copyright 2016 Medoly
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


class TemplateEngine(object):
    """Tempate engine info class"""

    def __init__(self, name):
        #: check whether is selene template
        if name != "selene":
            self.name = name + "t"
        else:
            self.name = name

        #: tempalte adapter module path
        self.module_path = "medoly.template.impl." + self.name

        #:  template loader, ui container, ui module class
        classes = _import_template_classes(self.module_path, name)
        self.loader_cls = classes[0]
        if self.loader_cls is None:
            raise NotImplementedError("Cant find the template engine adpater for {}".format(name))
        self.ui_container_cls = classes[1]
        self.ui_support = False

        if self.ui_container_cls:
            self.ui_module_cls = classes[2]
            self.ui_support = True

    def create_template_loader(self, directories, ui_container, settings):
        """Create template loader

        :param directories: the template root paths
        :type directories: list[string]
        :param ui_container: the ui container
        :param settings: the template loader settings
        :type settings: dict
        :returns: template loader
        """
        if self.ui_support:
            return self.loader_cls(directories, ui_container=ui_container, **settings)
        else:
            return self.loader_cls(directories, **settings)


def _import_template_classes(module_path, name):
    """Import  template classes from module"""
    loader = name.capitalize() + "Loader"
    classnames = [loader, "UIContainer", "UIModule"]
    m = __import__(module_path, globals(), locals(), classnames)
    return [getattr(m, classname, None) for classname in classnames]
