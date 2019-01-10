// Copyright (c) 2018, Maintenance and Repair Services and contributors
// For license information, please see license.txt

frappe.ui.form.on('MRS Settings', {
		onload: function(frm) {
	frm.set_query('default_account', function(doc) {
			return {
				filters: {
					"report_type": "Balance Sheet",
					"account_type" : "Receivable",
					"is_group" : 0
				}
			};
		});

	frm.set_query('income_account', function(doc) {
			return {
				filters: {
					"account_type" : "Income Account",
					"is_group" : 0
				}
			};
		});
},
	refresh: function(frm) {
		frm.set_df_property("default_account", "reqd", 0);

	},
	hourly:function(frm) {
		if (frm.doc.hourly == 1) 
			frm.set_value("dailly",0);	
	},
	dailly:function(frm) {
		if (frm.doc.dailly == 1) 
			frm.set_value("hourly",0);		
	},
	manual_process:function(frm) {
		if (frm.doc.manual_process == 1) 
			frm.set_value("auto_creation_process",0);	
	},
	auto_creation_process:function(frm) {

		if (frm.doc.auto_creation_process == 1) {
			frm.set_value("manual_process",0);	
			frm.set_df_property("default_account", "reqd", 1);
			}
		else frm.set_df_property("default_account", "reqd", 0);
	
	},
});
