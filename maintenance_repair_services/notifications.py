# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

def get_notification_config():
	return {
		"for_doctype": {
			"Maintenance Order": "maintenance_repair_services.notifications.get_expiry_orders",
		}
	}



def get_expiry_orders():
	if frappe.db.get_value("MRS Settings", None, "hourly") == '1':
		hourly = frappe.db.get_value("MRS Settings", None, "expiry_warning_durati")
		if hourly:	
			return frappe.db.sql("""\
				SELECT count(*)
				FROM `tabMaintenance Order`
				WHERE status not in ('Completed', 'Canceled')
				AND TIMESTAMPDIFF(HOUR, CURDATE(), end_date) <=%s
				""",hourly)[0][0]

	if frappe.db.get_value("MRS Settings", None, "dailly") == '1':
		dailly = frappe.db.get_value("MRS Settings", None, "expiry_warning_durati2")
		if dailly:	
			return frappe.db.sql("""\
				SELECT count(*)
				FROM `tabMaintenance Order`
				WHERE status not in ('Completed', 'Canceled')
				AND DATEDIFF(CURDATE(),end_date) <=%s
				""",dailly)[0][0]
