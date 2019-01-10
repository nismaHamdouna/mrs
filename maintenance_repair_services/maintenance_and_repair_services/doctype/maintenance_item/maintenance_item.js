// Copyright (c) 2018, Products Maintenance and contributors
// For license information, please see license.txt

frappe.ui.form.on('Maintenance Item', {

	
	refresh: function(frm) {
	if(frappe.defaults.get_default("customer")){
		frm.set_value("customer",frappe.defaults.get_default("customer"));
		frm.refresh_field("customer");
frappe.defaults.set_user_default_local("customer",null);
}
	if(frm.doc.customer){
	frappe.route_options={"customer":frm.doc.customer}; 
}
	frm.fields_dict.product_category.get_query = function() {
			return {
				filters:{
					'active': 1
				}
			}
		}
 		if (!frm.doc.__islocal) {

			var info = frm.doc;
			console.log(info);
			if (!frm.doc.__islocal) {

		frappe.call({
			method: "maintenance_repair_services.maintenance_and_repair_services.doctype.maintenance_item.maintenance_item.get_dashboard",
			args: {
				name: frm.doc.name
			},
			callback: function (r) {
				if(r.message){
					console.log(r.message);
					var total = r.message.total;
					var prepaid = r.message.prepaid;
					var total_paid=r.message.total_paid;
					var orders = r.message.orders;
					var c_orders = r.message.c_orders;
				frm.dashboard.stats_area_row.empty();
				frm.dashboard.add_indicator(__('Total Orders: {0}',
						[orders]), 'blue');
				frm.dashboard.add_indicator(__('Completed Orders: {0}',
						[c_orders]), 'orange');
									console.log("ssss");
				frm.dashboard.add_indicator(__('Total : {0}',
						[total]), 'green');
				
				frm.dashboard.add_indicator(__('Total Prepaid: {0}',
						[prepaid]), 'red');
				frm.dashboard.add_indicator(__('Total paid: {0}',
						[total_paid]), 'green');
				frm.dashboard.add_indicator(__('Total Remain : {0}',
						[total-total_paid]), 'red');



					}
		 		}		
	        	});
		}
			//console.log(erpnext.utils.set_party_dashboard_indicators(frm));
		}

	},
	onload: function(frm) {

		frm.set_query('item_type', function(doc) {
				return {
					filters: {
						"active": 1,
						"item_category" : frm.doc.item_category
					}
				};
			});
},
	barcode: function(frm){
		if(frm.doc.barcode){
			frm.set_df_property('barcode_html', 'options','<img style="float:left;" width="30%" src="https://barcode.tec-it.com/barcode.ashx?data='+frm.doc.barcode+'&code=Code128&dpi=96&dataseparator=%27%20alt=%27Barcode%20Generator%20TEC-IT"/>');

}
}
});
