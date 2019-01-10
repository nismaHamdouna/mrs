// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// render
frappe.listview_settings['Maintenance Order'] = {
	filters: [["status","!=","Completed"],["docstatus","<","2"]]
};
