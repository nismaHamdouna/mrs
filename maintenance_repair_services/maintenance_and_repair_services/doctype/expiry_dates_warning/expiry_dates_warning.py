# -*- coding: utf-8 -*-
# Copyright (c) 2018, Maintenance and Repair Services and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_hours, now,now_datetime


class ExpiryDatesWarning(Document):
	pass

@frappe.whitelist(allow_guest=True)
def expiry_duration():
	hourly=0
	dailly=0
	if frappe.db.get_value("MRS Settings", None, "hourly") == '1':
		hourly = frappe.db.get_value("MRS Settings", None, "expiry_warning_durati")
		#time_now = frappe.utils.now_datetime().strftime('%H:%M:%S')
		#downtime = time_diff_in_hours(time_now, expiry_warning_durati)
		#hourly= round(downtime, 2)
		#return hourly

	if frappe.db.get_value("MRS Settings", None, "dailly") == '1':
		dailly = frappe.db.get_value("MRS Settings", None, "expiry_warning_durati2")

	return hourly, dailly
		
