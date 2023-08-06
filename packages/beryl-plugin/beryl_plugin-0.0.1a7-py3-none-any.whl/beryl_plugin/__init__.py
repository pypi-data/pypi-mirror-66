import abc

__version__ = "0.0.1-alpha.7"

class PluginBase(abc.ABC):
	def __init__(self, spawning_class, display_name, ID):
		self._super_class = spawning_class
		self._child_display_name = display_name
		self.ID = ID

	# Required to override
	@abc.abstractmethod
	def stop(self):
		"""Called when the plugin is no longer needed. Should properly close any open streams.
		"""
		pass

	# API Methods
	# Configurations
	def get_current_config(self):
		return self._super_class.get_current_config(self)
	
	# Display related methods
	def get_plugin_display(self):
		return self._super_class.get_plugin_display(self)

class Event:
	key = "key"
	loop = "loop"
	period_change = "period change"
	config_change = "config change"

	_all_events = [key, loop, period_change, config_change]
