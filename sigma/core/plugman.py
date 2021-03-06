import os

from .logger import create_logger
from .plugin import Plugin


class PluginManager(object):
    def __init__(self, bot):
        self.bot         = bot
        self.client      = self.bot
        self.cooldown    = bot.cooldown
        self.db          = bot.db
        self.music       = bot.music
        self.cooldown = bot.cooldown
        self.log         = create_logger('Plugin Manager')
        self.plugin_dirs = []
        self.plugins     = []
        self.commands    = {}
        self.events = {
            'mention': {},
            'message': {},
            'member_join': {},
            'member_leave': {},
            'ready': {},
            'voice_update': {},
            'message_edit': {}
        }

        self.get_plugin_dirs()
        self.load_all()

    def load_plugin(self, path):
        plugin = Plugin(self.bot, path)

        if plugin.loaded:
            self.plugins.append(plugin)
            self.commands.update(plugin.commands)

            for ev_type, events in self.events.items():
                events.update(plugin.events[ev_type])

    def reload_plugin(self, pluginName):
        for plugin in self.plugins:
            if plugin.name == pluginName:
                try: plugin.reload_commands()
                except Exception as e:
                    raise Exception(e)
                return
        raise Exception("Plugin not found")

    def get_plugins(self):
        pluginList = ""
        for plugin in self.plugins:
            pluginList += plugin.name + ", "
        return pluginList

    def load_all(self):
        for path in self.plugin_dirs:
            self.load_plugin(path)

    def get_plugin_dirs(self):
        for root, dir, files in os.walk('sigma/plugins'):
            if 'plugin.yml' in files:
                self.plugin_dirs.append(root)
