from django.utils.importlib import import_module
from settings import INSTALLED_PLUGINS

for plugin in INSTALLED_PLUGINS:
    import_module('%s.plugin_hooks' % plugin)