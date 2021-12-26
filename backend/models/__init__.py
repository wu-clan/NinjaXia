# -*- coding: utf-8 -*-
import os
import sys
from importlib import import_module

from django.apps import config
from django.utils.module_loading import module_has_submodule

sys.path.append(str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# 将"models文件名"补充后再执行迁移
MODELS_MODULE_NAME = 'project', 'interface', 'case'


class AppConfigReset(config.AppConfig):
    if config.MODELS_MODULE_NAME:
        if type(MODELS_MODULE_NAME) == tuple:
            for model in MODELS_MODULE_NAME:
                config.MODELS_MODULE_NAME = model

                def import_models(self):
                    self.models = self.apps.all_models[self.label]
                    if module_has_submodule(self.module, config.MODELS_MODULE_NAME):
                        models_module_name = '%s.%s' % (self.name, config.MODELS_MODULE_NAME)
                        self.models_module = import_module(models_module_name)

    def import_models(self):
        self.models = self.apps.all_models[self.label]
        if module_has_submodule(self.module, config.MODELS_MODULE_NAME):
            models_module_name = '%s.%s' % (self.name, config.MODELS_MODULE_NAME)
            self.models_module = import_module(models_module_name)
