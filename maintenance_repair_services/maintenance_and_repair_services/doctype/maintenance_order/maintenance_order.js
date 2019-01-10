// Copyright (c) 2018, Products Maintenance and contributors
// For license information, please see license.txt

{% include 'erpnext/selling/sales_common.js' %}

frappe.ui.form.on('Maintenance Order', {
	on_submit: function(frm) {
	  
	var dialog = new frappe.ui.Dialog({
    'title':__("Payment Details"),
    'fields': [
        {'fieldname': 'ht', 'fieldtype': 'HTML'},
        {'fieldname': 'to_pay', 'fieldtype': 'Check', 'label': 'To Pay?',"default":1},
        {'fieldtype': "Section Break"},
        {'fieldname': 'status', 'fieldtype': 'Select', 'label': 'Status',"options": "\nWaiting\nCanceled\nUnder maintenance\nCompleted"},
        {'fieldname': 'total', 'fieldtype': 'Currency', 'label': 'Total',"default":cur_frm.doc.total,read_only: 1},
       //{'fieldname': 'cheque_no', 'fieldtype': 'Int', 'label': 'Cheque/Reference No',"depends_on":"to_pay"},
        {'fieldname': 'prepaid', 'fieldtype': 'Currency', 'label': 'Prepaid',"default":cur_frm.doc.prepaid,read_only: 1},
        {'fieldname': 'paid', 'fieldtype': 'Currency', 'label': 'To Paid',"default":cur_frm.doc.total-cur_frm.doc.prepaid, 'depends_on':'eval:doc.to_pay'},
        //{'fieldname': 'cheque_date', 'fieldtype': 'Date', 'label': 'Cheque/Reference Date',"depends_on":"to_pay"},

    ],
    primary_action_label:__('Confirm'),
    primary_action: function(){
		var d= dialog.get_values();
console.log(d);
		var status = d.status;

		
		var to_pay = d.to_pay;
		var paid = d.paid; console.log(paid)

	console.log(to_pay)
		dialog.hide(); //to_pay=0;
	    if (to_pay==1){
		frappe.call({
			method: 'pay_order',
			doc: frm.doc,
			args:{'paid':paid,'status':status},
			callback: function (r) {		
				console.log(r)
				frm.refresh();
				}
		});
	    }
	}
	});
	dialog.fields_dict.ht.$wrapper.html('<div> Your payment details, You should enter rhe pay,ent value and confirm it </div>');
	dialog.show();

	},
	refresh: function(frm) {
		 frappe.meta.get_docfield("Maintenance Order Items","qty", cur_frm.doc.name).read_only = 0;
 if (!frm.doc.__islocal) {

			
				frappe.call({
			method: "maintenance_repair_services.maintenance_and_repair_services.doctype.maintenance_order.maintenance_order.get_dashboard",
			args: {
				name: frm.doc.name
			},
			freeze:true,
			callback: function (r) {
				if(r.message){
					var total = r.message.total;
					var prepaid = r.message.prepaid;
					var total_paid=r.message.total_paid;
				frm.dashboard.stats_area_row.empty();
				frm.dashboard.add_indicator(__('Total : {0}',
						[total]), 'orange');
				
				frm.dashboard.add_indicator(__('Total Prepaid: {0}',
						[prepaid]), 'blue');
				frm.dashboard.add_indicator(__('Total paid: {0}',
						[total_paid]), 'green');
									console.log("saaa");
				frm.dashboard.add_indicator(__('Total Remain : {0}',
						[total-total_paid]), 'red');


					}
		 		}		
	        	});

		}
	
	if(frm.doc.customer){
	frappe.route_options={"customer":frm.doc.customer}; 
		}
	},	
	customer: function(frm) {
		frm.set_value('item_code','');
		if (frm.doc.customer){
		frappe.defaults.set_user_default_local("customer",frm.doc.customer)
		}
	},
	onload: function(frm) {
	frappe.db.get_value('Maintenance Section', null,'section_name', function(r) {
			console.log(r)
			if (!r)
				frm.toggle_display("section", false); 
			else
				frm.toggle_display("section", true); 
		});
			

	if (frappe.user.has_role("Maintenance Manager"))
		frm.toggle_display("products_details", true); 
	else if (!frappe.user.has_role("Maintenance Manager") && frappe.user.has_role("Customer"))
		frm.toggle_display("products_details", false); 

	frm.fields_dict.item_code.get_query = function() {
			return {
				filters:{
					'customer': frm.doc.customer
				}
			}
		}
frappe.route_options={};


	},

});


frappe.ui.form.on("Maintenance Order Items", {
	item_code: function(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
			if (row.item_group=='Services') 
				if (row.qty > 1){
					//frappe.msgprint(__("Service Item quantity could not be more than 1"))
					row.qty =1;
					frm.toggle_display("qty", true)
		 frappe.meta.get_docfield("Maintenance Order Items","qty", cur_frm.doc.name).read_only = 1;
					}
			
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Item Price",
					fieldname: "price_list_rate",
					filters: { item_code:row.item_code,
						   selling:1  }
				},
				callback: function(r) {
					if (r.message) {
			if (row.qty < 1)
			row.rate = r.message.price_list_rate * row.qty;
			else if (row.qty >= 1) row.rate = r.message.price_list_rate;

			row.net_rate = row.rate;
			row.amount = flt(row.rate * row.qty);
			refresh_field("qty", cdn, "product_for_maintenance");
			refresh_field("rate", cdn, "product_for_maintenance");
			refresh_field("net_rate", cdn, "product_for_maintenance");
			refresh_field("amount", cdn, "product_for_maintenance");
			}
		}});
	},
	qty: function(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
			if (row.item_group=='Services') 
				if (row.qty > 1){
					//frappe.msgprint(__("Service Item quantity could not be more than 1"))
					row.qty =1;
					refresh_field("qty", cdn, "product_for_maintenance");
					frm.toggle_display("qty", true)
		 frappe.meta.get_docfield("Maintenance Order Items","qty", cur_frm.doc.name).read_only = 1;
					return false;
					}

			if (row.qty < 1)
			row.rate = row.rate * row.qty;
			else if (row.qty >= 1) row.rate = row.rate;

			row.net_rate = row.rate;
			row.amount = flt(row.rate * row.qty);
			refresh_field("qty", cdn, "product_for_maintenance");
			refresh_field("rate", cdn, "product_for_maintenance");
			refresh_field("net_rate", cdn, "product_for_maintenance");
			refresh_field("amount", cdn, "product_for_maintenance");

		
	},
	amount: function(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
			row.net_rate = row.rate;
			row.amount = flt(row.rate * row.qty);
			refresh_field("net_rate", cdn, "product_for_maintenance");
			refresh_field("amount", cdn, "product_for_maintenance");

		
	},
	rate: function(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
			row.net_rate = row.rate;
			row.amount = flt(row.rate * row.qty);
			refresh_field("net_rate", cdn, "product_for_maintenance");
			refresh_field("amount", cdn, "product_for_maintenance");

		
	}

});


erpnext.selling.MaintenanceController = erpnext.selling.SellingController.extend({
onload: function(doc, dt, dn) {
		var me = this;
		this._super(doc, dt, dn);


	},
	refresh: function(doc, dt, dn) {
		this._super(doc, dt, dn);
}
});

