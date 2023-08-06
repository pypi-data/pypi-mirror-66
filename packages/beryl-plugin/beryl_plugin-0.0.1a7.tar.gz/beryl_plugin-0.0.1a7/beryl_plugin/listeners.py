from . import Event

def beryl_plugin(plugin_class):
	plugin_class._is_beryl_plugin = True
	return plugin_class

def on_key(*keys):
	def function(func):
		func._is_beryl_handler = True
		func._beryl_event = Event.key
		func._keys = keys
		return func
	return function

def on_period_change(func):
	func._is_beryl_handler = True
	func._beryl_event = Event.period_change
	return func

def on_loop(func):
	func._is_beryl_handler = True
	func._beryl_event = Event.loop
	return func

def on_config_change(func):
	func._is_beryl_handler = True
	func._beryl_event = Event.config_change
	return func
