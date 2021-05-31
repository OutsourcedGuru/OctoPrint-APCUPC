# coding=utf-8
from __future__ import absolute_import
from subprocess import check_output
from subprocess import call, Popen, PIPE
from octoprint.settings import settings, valid_boolean_trues
import flask
import octoprint.plugin
import os
import re

class ApcupcPlugin(octoprint.plugin.SettingsPlugin,
                   octoprint.plugin.AssetPlugin,
									 octoprint.plugin.SimpleApiPlugin,
									 octoprint.plugin.StartupPlugin,
                   octoprint.plugin.TemplatePlugin):

	def get_settings_defaults(self):
		return dict(
			init =                                False,
			isRaspi2B =                           False,
			isRaspi3B =                           False,
			isRaspi3Bplus =                       False,
			isRaspi4B =                           False,
			isRaspi400 =                          False,
			cpuRevision =                         'unknown',
			piModel =                             'unknown'
		)

	def get_template_vars(self):
		return dict(
			init =                                self._settings.get(["init"]),
			isRaspi2B =                           self._settings.get(["isRaspi2B"]),
			isRaspi3B =                           self._settings.get(["isRaspi3B"]),
			isRaspi3Bplus =                       self._settings.get(["isRaspi3Bplus"]),
			isRaspi4B =                           self._settings.get(["isRaspi4B"]),
			isRaspi400 =                          self._settings.get(["isRaspi400"]),
			cpuRevision =                         self._settings.get(["cpuRevision"]),
			piModel =                             self._settings.get(["piModel"])
		)

	def get_template_configs(self):
		return [dict(type="settings", custom_bindings=False)]

	def get_assets(self):
		return dict(
			js =                                  ["js/apcupc.js"],
			css =                                 ["css/apcupc.css"],
			less =                                ["less/apcupc.less"]
		)

	def get_api_commands(self):
		return dict(save=["init"])

	def on_api_command(self, command, data):
		if command == "save":
			self._logger.info("save init in settings")
			progRev =                             Popen(["cat", "/proc/cpuinfo"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
			cpuinfo, err =                        progRev.communicate(b"")
			matchObj =                            re.search(r'^Revision\s+:\s+(.*)$', cpuinfo, re.M)
			cpuRevision =                         matchObj.group(1) if matchObj else ""
			piModel =                             self.switch(cpuRevision, 'unknown')
			s =                                   settings()
			s.setBoolean(["plugins", "apcupc", "init"],           True)
			s.setBoolean(["plugins", "apcupc", "isRaspi2B"],      True if piModel == "Raspi2B" else False)
			s.setBoolean(["plugins", "apcupc", "isRaspi3B"],      True if piModel == "Raspi3B" else False)
			s.setBoolean(["plugins", "apcupc", "isRaspi3Bplus"],  True if piModel == "Raspi3B+" else False)
                        s.setBoolean(["plugins", "apcupc", "isRaspi4B"],      True if piModel == "Raspi4B" else False)
                        s.setBoolean(["plugins", "apcupc", "isRaspi400"],     True if piModel == "Raspi400" else False)
			s.set(["plugins",        "apcupc", "cpuRevision"],    cpuRevision)
			s.set(["plugins",        "apcupc", "piModel"],        piModel)
			s.save()

	def switch(self, key, default):
		case = {
			'0007':   'RaspiA',
			'0008':   'RaspiA',
			'0009':   'RaspiA',
			'0012':   'RaspiA+',
			'0015':   'RaspiA+',
			'0002':   'RaspiB',
			'0003':   'RaspiB',
			'0004':   'RaspiB',
			'0005':   'RaspiB',
			'0006':   'RaspiB',
			'000d':   'RaspiB',
			'000e':   'RaspiB',
			'000f':   'RaspiB',
			'0010':   'RaspiB+',
			'0013':   'RaspiB+',
                        '900021': 'RaspiB+',
			'900032': 'RaspiB+',
			'a01041': 'Raspi2B',
			'a21041': 'Raspi2B',
			'a21042': 'Raspi2B',
                        'a22042': 'Raspi2B',
                        'a01040': 'Raspi2B',
                        'a01041': 'Raspi2B',
                        'a02042': 'Raspi2B',
			'a02082': 'Raspi3B',
			'a22082': 'Raspi3B',
			'a020d3': 'Raspi3B+',
			'9000c1': 'ZeroW',
			'900092': 'Zero',
			'900093': 'Zero',
                        '920093': 'Zero',
                        '920092': 'Zero',
			'9020e0': 'Raspi3A+',
                        '0011':   'ComputeModule1',
                        '0014':   'ComputeModule1',
                        '900061': 'ComputeModule1',
                        'a020a0': 'ComputeModule3',
                        'a220a0': 'ComputeModule3',
                        'a32082': 'Raspi3B',
                        'a52082': 'Raspi3B',
                        'a22083': 'Raspi3B',
                        'a02100': 'ComputeModule3+',
                        'a03111': 'Raspi4B',
                        'b03111': 'Raspi4B',
                        'b03112': 'Raspi4B',
                        'b03114': 'Raspi4B',
                        'c03111': 'Raspi4B',
                        'c03112': 'Raspi4B',
                        'c03114': 'Raspi4B',
                        'd03114': 'Raspi4B',
                        'c03130': 'Raspi400',
		}
		return case.get(key, default)

	def on_startup(self, host, port):
		pass

	def get_update_information(self):
		return dict(
			apcupc = dict(
				displayName =                       "Apcupc Plugin",
				displayVersion =                    self._plugin_version,
				type =                              "github_release",
				user =                              "OutsourcedGuru",
				repo =                              "OctoPrint-APCUPC",
				current =                           self._plugin_version,
				pip =                               "https://github.com/OutsourcedGuru/OctoPrint-APCUPC/archive/{target_version}.zip"
			)
		)

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ApcupcPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

