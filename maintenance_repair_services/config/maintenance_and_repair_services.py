# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Reception"),
			"items": [
			       {
					"type": "doctype",
					"name": "Customer",
					"description": _("Customer.")
				},
			       {
					"type": "doctype",
					"name": "Maintenance Item",
					"description": _("Maintenance Item.")
				},

				{
					"type": "doctype",
					"name": "Maintenance Order",
					"description": _("Maintenance Order."),
				}, 
			]
		},
				{
			"label": _("Maintenance"),
			"icon": "fa fa-star",
			"items": [
							       {
					"type": "doctype",
					"name": "Delivery Note",
					"label": _("Request delivery of products"),
					"description": _("Request delivery of products")
				},
				{
					"type": "doctype",
					"name": "Maintenance Stuff",
					"description": _("Maintenance Stuff."),
				}, 

			       {
					"type": "doctype",
					"name": "Sales Invoice",
					"description": _("Sales Invoice.")
				},
				{
					"type": "doctype",
					"name": "Customers Feedback",
					"label": _("Customers Feedback"),
					"description": _("Visit report for maintenance call.")
				},
			       {
					"type": "doctype",
					"name": "Expiry Dates Warning",
					"description": _("Expiry Date Warning.")
				},

			]
		},
		{
			"label": _("Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "Customize Form",
					"label": _("Customize Form"),
					"description": _("Customize Form.")
				},
			       {
					"type": "doctype",
					"name": "Item Category",
					"description": _("Item Category")
				},
 				{
					"type": "doctype",
					"name": "Item Type",
					"description": _("Item Type")
				},
			       {
					"type": "doctype",
					"name": "Maintenance Section",
					"description": _("Maintenance Section.")
				},
				{
					"type": "doctype",
					"name": "MRS Settings",
					"label": _("MRS Settings"),
					"description": _("MRS Settings.")
				},
			
			]
		},
		{
			"label": _("Report"),
			"items": [

				{
					"type": "report",
					"is_query_report": True,
					"name": "Maintenance Item",
					"doctype": "Maintenance Item"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Maintenance Orders",
					"doctype": "Maintenance Order"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Maintenance Staff",
					"doctype": "Maintenance Staff"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Request delivery of products",
					"doctype": "Request delivery of products"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Customers Feedback",
					"doctype": "Customers Feedback"
				},
			
			]
		},


	
	]
