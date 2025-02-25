#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : src/ampel/contrib/hu/examples/t0/ExampleFilter.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 22.09.2018
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from ampel.base.abstract.AbsAlertFilter import AbsAlertFilter
from ampel.pipeline.logging.LoggingUtils import LoggingUtils

class ExampleFilter(AbsAlertFilter):
	"""
	REQUIREMENTS:
	-------------
	A T0 filter class must (otherwise exception will be throwed):
	* inherit the abstract parent class 'AbsAlertFilter'
	* implement the following two functions:
		-> __init__(self, on_match_t2_units, base_config=None, run_config=None, logger=None)
		-> apply(self, ampel_alert)
	"""

	def __init__(self, on_match_t2_units, base_config=None, run_config=None, logger=None):
		"""
		Mandatory implementation.
		See the jupyter notebook "Understanding T0 Filters"

		Parameters:
		'on_match_t2_units': list of t2 unit ids (strings) 
		'base_config': dict instance loaded from the ampel config
		'run_config': dict instance loaded from the ampel config
		'logger': logger instance (python module logging)
		"""

		# Instance variable holding reference to provider logger 
		self.logger = LoggingUtils.get_logger() if logger is None else logger

		# Logging example
		self.logger.info("Please use this logger object for logging purposes")
		self.logger.debug("The log entries emitted by this logger will be stored into the Ampel DB")
		self.logger.debug("This logger is to be used 'as is', please don't change anything :)")

		# TODO: explain
		self.on_match_t2_units = on_match_t2_units

		# Example: 'magpsf' (see the jupyter notebook "Understanding T0 Filters")
		self.filter_field = base_config['attrName']

		# Example: 18 (see the jupyter notebook "Understanding T0 Filters")
		self.threshold = run_config['threshold']


	def apply(self, ampel_alert):
		"""
		Mandatory implementation.
		To exclude the alert, return *None*
		To accept it, either 
			* return self.on_match_t2_units
			* return a custom list of t2 unit ids (strings) 
			 -> the custom list must be a subset of self.on_match_t2_units, 
			    it cannot contain other/new t2 unit ids.

		In this example filter, any measurement of a transient 
		brighter than a fixed magnitude threshold will result 
		in this transient being inserted into ampel.
		"""

		# One way of filtering alerts based on fixed mag threshold
		# (for other means of achiving the same results, please 
		# see the jupyter notebook "Understanding T0 Filters")
		for pp in ampel_alert.get_photopoints():

			# Example: 
			# self.filter_field: "magpsf"
			# self.threshold: 18
			if pp[self.filter_field] < self.threshold :
				return self.on_match_t2_units

		return None
