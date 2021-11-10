# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Excel ERPNext",
			"color": "grey",
			"icon": "fa fa-cloud",
			"type": "module",
			"label": _("Excel")
		},
		{
			"module_name": "ArcApps",
			"color": "grey",
			"icon": "fa fa-cloud",
			"type": "module",
			"label": _("ArcApps")
		},
		{
			"module_name": "Excel Reports",
			"color": "grey",
			"icon": "fa fa-cloud",
			"type": "module",
			"label": _("Reports")
		}
	]
