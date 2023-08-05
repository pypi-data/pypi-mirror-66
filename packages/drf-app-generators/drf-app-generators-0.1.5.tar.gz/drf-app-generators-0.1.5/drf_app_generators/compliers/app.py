import os
import copy
import yaml

from django.conf import settings

from drf_app_generators.compliers.model import ModelMeta


class AppOptions(object):

    models: [str] = []  # a list of model names
    api_doc: bool = False
    nested: bool = False
    force: bool = False

    def __init__(self, models=[], api_doc=False, nested=False, force=False):
        self.models = models
        self.api_doc = api_doc
        self.nested = nested
        self.force = force

    def to_json(self) -> dict:
        return self.__dict__


class RequiredFactories(object):
    code_line: str = None
    app_name: str = None
    model_names: [str] = None

    def __init__(self, app_name=None, model_names=[]):
        self.app_name = app_name
        self.model_names = model_names


class AppConfig(object):
    """
    This contains all configuration to generate/update a Django app.
    """
    name: str = None
    name_capitalized: str = None
    options: AppOptions = AppOptions()
    models_meta: [ModelMeta] = []
    force: bool = False  # force to override.

    # Summary required libraries and modules from model meta.
    factory_required_libs: [str] = []
    factory_required_modules: [str] = []

    def __init__(self, name=None, options=None, init=True):
        self.name = name
        self.name_capitalized = self.name.capitalize()
        self.options = options
        self.init = init  # Init app the first time.
        self.models_meta = []

        if self.init:
            # Build model meta for the first time.
            self._build_models_meta()

    def set_models_meta(self, models_meta: [object]):
        """
        Set a list of models meta to app.
        """
        self.models_meta = models_meta

        for model_meta in models_meta:
            # Summary required libraries & modules for factory.
            self.factory_required_libs = set().union(
                self.factory_required_libs,
                model_meta.factory_required_libs
            )
            self._build_required_factories(model_meta.factory_required_modules)

    def _build_models_meta(self):
        """
        Create models meta from options.
        """
        model_names = []

        if self.options and self.options.models:
            model_names = self.options.models

        for model_name in model_names:
            # Build the model meta.
            model_meta = ModelMeta(model=None)
            model_meta.build_from_name(name=model_name)
            self.models_meta.append(model_meta)

    def _build_required_factories(self, required_modules=[]):
        for module in required_modules:
            if self._is_module_from_current_app(module):
                continue

            # Find the existed module on the list.
            existed_module = self._find_factory_required_module_by_app(
                app_name=module.app_name)

            if existed_module:
                # add model name to existed module
                existed_module.model_names.append(module.model_name)
            else:
                required_factory = RequiredFactories(
                    app_name=module.app_name,
                    model_names=[module.model_name],
                )
                self.factory_required_modules.append(required_factory)

    def _find_factory_required_module_by_app(self, app_name=None):
        required_module = None

        if app_name is None:
            return required_module

        for module in self.factory_required_modules:
            if module.app_name == app_name:
                required_module = module
                break

        return required_module

    def _is_module_from_current_app(self, module):
        return module.app_name.lower() == self.name.lower()

    def to_json(self) -> dict:
        """
        Dump this class to JSON.
        """
        obj = copy.copy(self.__dict__)
        obj['options'] = self.options.to_json()
        obj['models_meta'] = []

        for model_meta in self.models_meta:
            model_obj = model_meta.to_json()
            obj['models_meta'].append(model_obj)

        return obj

    def write_to_yaml(self):
        """
        Write the JSON data to yaml.
        """
        base_dir = settings.BASE_DIR
        data = self.to_json()

        if base_dir:
            base_dir = os.path.join(base_dir, self.name, 'meta.yaml')
        else:
            base_dir = os.path.join(os.getcwd(), self.name, 'meta.yaml')

        with open(f'{base_dir}', 'w') as fp:
            fp.write(yaml.dump(data, indent=4))
