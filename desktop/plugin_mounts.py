from backend.plugin_helpers import PluginMount


class SettingsMenuItem:
    """
    Mount point for plugins which need to registrar items in the settings menu

    Plugins implementing this reference should provide the following attributes:

    label    The label of the button
    setting  Identifier of the setting
    url      Url of the view
    """
    __metaclass__ = PluginMount