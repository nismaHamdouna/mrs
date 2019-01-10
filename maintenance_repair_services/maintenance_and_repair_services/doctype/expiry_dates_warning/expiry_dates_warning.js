// Copyright (c) 2018, Maintenance and Repair Services and contributors
// For license information, please see license.txt

frappe.ui.form.on('Expiry Dates Warning', {
	onload: function(frm) {
   var existed= false;
//if(frm.is_new()) {
		

		frappe.call({
				method: "maintenance_repair_services.maintenance_and_repair_services.doctype.expiry_dates_warning.expiry_dates_warning.expiry_duration",
				callback: function(r) {
					console.log(r)
				var hourly =r.message[0];
				var dailly =r.message[1];
				
				

 			frappe.call({
				method: "frappe.client.get_list",
				args: {
					doctype: "Maintenance Order",
					filters: [["status","!=","Completed"],["docstatus","<","2"]] ,
					fields:["name","status","customer","end_date","full_name"],
					
				},
				callback: function(r) {
	//console.log(r);
			if (r !=undefined){
			var uncompleted_orders = $.map(frm.doc.uncompleted_orders, function(d) { return d.name });
				frm.set_value("uncompleted_orders", []);

		for (var i=0; i< r.message.length; i++) {
			if (uncompleted_orders.indexOf(r.message[i].name) === -1) {
			        existed= false;                              // console.log(frm.doc.uncompleted_orders.length);
				for (var j=0; j< frm.doc.uncompleted_orders.length; j++) {
					if (r.message[i].name == frm.doc.uncompleted_orders[j].order)
			                 	existed=true;}
			if (!existed){ 
				total_time = frappe.datetime.get_hour_diff( r.message[i].end_date, frappe.datetime.now_datetime());
				total_day  = frappe.datetime.get_day_diff( r.message[i].end_date, frappe.datetime.now_datetime());
				//minutes= moment(frappe.datetime.now_datetime()).diff(moment(r.message[i].end_date),"minutes")
				//var hours = Math.trunc(minutes/60);
				//console.log(total_time);
				//console.log(total_day);
				var total =0;
				var diff= 0;
				if (hourly != 0) {  total = total_time; diff=hourly;}
				else if (dailly != 0){ total = total_day; diff=dailly;}

			//if(total <= diff)
			//		{
				//if (hourly != 0) 
					if(total <= diff)

					{	
			var row = frappe.model.add_child(frm.doc, frm.fields_dict.uncompleted_orders.df.options, frm.fields_dict.uncompleted_orders.df.fieldname);
				row.order = r.message[i].name;
				row.status = r.message[i].status;
				row.customer = r.message[i].customer;
				row.end_date = r.message[i].end_date; 
				row.assign_to = r.message[i].full_name; 
					}
				}

				}

			}
		frm.refresh_field('uncompleted_orders');}

}

});

//////
}

});
	//}

},
	refresh: function(frm) {}
});




frappe.ui.form.on("Uncompleted Orders",  {

	recomplete: function(frm,cdt,cdn) {
	d = locals[cdt][cdn];
		frappe.set_route("Form", "Maintenance Order",d.order);

}

});
