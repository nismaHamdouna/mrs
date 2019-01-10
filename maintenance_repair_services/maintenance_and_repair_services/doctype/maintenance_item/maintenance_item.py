# -*- coding: utf-8 -*-
# Copyright (c) 2018, Products Maintenance and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class MaintenanceItem(Document):
	pass
		
		


@frappe.whitelist()
def get_dashboard(name):
	if name:
		item=frappe.get_doc("Maintenance Item",name)
		if item:
			prepaid=0
			total=0
			total_paid=0
			orders=frappe.get_list("Maintenance Order",['name'],filters={'item_code':item.name,'docstatus':['<',2]})
			for order in orders:
				oo=frappe.get_doc("Maintenance Order",order.name)
				prepaid+=oo.prepaid
				if oo.total:
					total+=oo.total
				if oo.invoice:
					sales_invoices=frappe.get_list("Payment Entry Reference",['parent'],filters={'reference_name':oo.invoice,'reference_doctype':"Sales Invoice"})

					if sales_invoices:
						for sales in sales_invoices:
							ss=frappe.get_doc("Payment Entry",sales.parent)
							total_paid+=ss.paid_amount
				else:
					total_paid=prepaid


			orders_C=frappe.get_list("Maintenance Order",['name'],filters={'item_code':item.name,'docstatus':1})
			item.total_orders=len(orders)
			item.completed_orders=len(orders_C)
			item.total_amount=total
			item.total_prepaid=prepaid
			item.total_paid=total_paid
			item.flags.ignore_permissions = True
			#item.save()
			
			return {'total' : total,
				'prepaid' : prepaid,
				'total_paid':total_paid,
				'orders' : len(orders),
				'c_orders' : len(orders_C)
				} 
			
		
			
					

		
