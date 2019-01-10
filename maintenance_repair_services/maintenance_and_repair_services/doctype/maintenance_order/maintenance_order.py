# -*- coding: utf-8 -*-
# Copyright (c) 2018, Products Maintenance and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, nowdate, getdate
from frappe.model.document import Document
from frappe import _,msgprint
from erpnext import get_default_currency
from erpnext.controllers.queries import get_income_account
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry, get_company_defaults
from erpnext.accounts.utils import get_account_currency
import datetime
from erpnext.accounts.party import validate_party_accounts,get_party_account_currency, get_dashboard_info, get_timeline_data # keep this
from erpnext.accounts.utils import get_fiscal_year
from erpnext import get_default_currency, get_company_currency

#from erpnext.controllers.selling_controller import SellingController

form_grid_templates = {
	"items": "templates/form_grid/item_grid.html"
}

class MaintenanceOrder(Document):
	def onload(self):
		self.load_dashboard_info()
	frappe.route_options={}; 

	def load_dashboard_info(self):
		#info = get_dashboard_info("Customer", self.name)
		party=self.customer
		party_type="Customer"
		current_fiscal_year = get_fiscal_year(nowdate(), as_dict=True)
		company = frappe.db.get_default("company") or frappe.get_all("Company")[0].name
		party_account_currency = get_party_account_currency(party_type, party, company)
		company_default_currency = get_default_currency() \
			or frappe.db.get_value('Company', company, 'default_currency')

		if party_account_currency==company_default_currency:
			total_field = "base_grand_total"
		else:
			total_field = "grand_total"

		doctype = "Sales Invoice" 

		billing_this_year = frappe.db.sql("""
			select sum({0})
			from `tab{1}`
			where {2}=%s and docstatus=1 and posting_date between %s and %s
		""".format(total_field, doctype, party_type.lower()),
		(party, current_fiscal_year.year_start_date, current_fiscal_year.year_end_date))

		total_unpaid = frappe.db.sql("""
			select sum(debit_in_account_currency) - sum(credit_in_account_currency)
			from `tabGL Entry`
			where party_type = %s and party=%s""", (party_type, party))

		info = {}
		info["billing_this_year"] = flt(billing_this_year[0][0]) if billing_this_year else 0
		info["currency"] = party_account_currency
		info["total_unpaid"] = flt(total_unpaid[0][0]) if total_unpaid else 0
		if party_type == "Supplier":
			info["total_unpaid"] = -1 * info["total_unpaid"]

		return info
		self.set_onload('dashboard_info', info)

	def validate(self):
		isum= 0
		order_items= self.get_items()
		for i in order_items: 
			isum += i['amount']
	 	self.total= isum
		item=frappe.get_doc("Maintenance Item",self.item_code)
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
				pay=frappe.get_list("Payment Entry",['paid_amount','name'],filters={'reference_no':order.name})
				if pay:
					for p in pay:
						pp=frappe.get_doc("Payment Entry",p.name)
						total_paid=pp.paid_amount
				else:
					total_paid+=oo.prepaid
				

			orders_C=frappe.get_list("Maintenance Order",['name'],filters={'item_code':item.name,'docstatus':1})
			item.total_orders=len(orders)
			item.completed_orders=len(orders_C)
			item.total_amount=total
			item.total_prepaid=prepaid
			item.total_paid=total_paid
			item.flags.ignore_permissions = True
			item.save()
	def after_insert(self):
		worker=frappe.new_doc("Maintenance Prepaid")
		worker.maintenance_order=self.name
		worker.worker=frappe.session.user
		worker.date=datetime.datetime.now()
		worker.prepaid=self.prepaid
		worker.insert(ignore_permissions=True)
		

	def on_submit(self):
		debit_to = self.check_auto_process()
		if debit_to:
			order_items= self.get_items()
			isum= 0
			for i in order_items: 
				isum += i['amount']
			self.make_deliv_note(order_items, isum)
			self.make_sale_invoice(order_items, debit_to,isum)
			#self.create_payment_entry()

	def check_auto_process(self):
		debit_to,income_account = None, None
		manual_process= frappe.db.get_value("MRS Settings", None, "manual_process")
		auto_creation_process= frappe.db.get_value("MRS Settings", None, "auto_creation_process")
		manual_process= frappe.db.get_value("MRS Settings", None, "manual_process")
		if auto_creation_process == '0' and manual_process == '0':
			frappe.throw(_("you have to complete the Maintenance Settings"))
		if auto_creation_process == '1':
			debit_to= frappe.db.get_value("MRS Settings", None, "default_account")
			income_account= frappe.db.get_value("MRS Settings", None, "income_account")
		return debit_to


	def get_items(self):
		order_items =[]
		income_account= frappe.db.get_value("MRS Settings", None, "income_account")
		for items in self.product_for_maintenance:
			order_item={
				'item_code': items.item_code,
				'item_name': items.item_name,
				'description': items.description,
				'rate':items.rate,
				'amount':items.amount,
				'qty': items.qty,
				'uom':items.uom,
				"warehouse":items.warehouse,
				'income_account':income_account,#'4110 - Sales - ADM', #self.check_auto_process() or None,
				'base_rate':items.rate,
				'base_amount': items.base_amount,
				'conversion_factor':1,
				'sales_order':'',
				'delivery_note':'',
				'dn_detail':''
				#'billed_amt':items.amount
				}
			order_items.append(order_item)
		return order_items

	def make_deliv_note(self,order_items, isum):
		#frappe.msgprint(self.customer)
		delivery_note = frappe.new_doc('Delivery Note')
		delivery_note.update({
			"customer": self.customer,
			"customer_name": self.customer_name,
			"company": self.company,
			"price_list_currency":get_default_currency() or frappe.get_cached_value('Company',  company,  'default_currency'),
			"ignore_pricing_rule":0,
			"conversion_rate":1,
			"plc_conversion_rate":1,
			"total":isum,
			"net_total":isum,
			"base_total":isum,
			"base_net_total":isum,
			"base_grand_total":isum,
			"base_rounded_total":isum,
			"grand_total":isum,
			"rounded_total":isum,
			"items": order_items,
			"maintenance_order":self.name
			})
		delivery_note.set_missing_values(for_validate = True)
		delivery_note.insert(ignore_permissions=True)
		delivery_note.submit()
		self.delivery_note = delivery_note.name
		frappe.msgprint(_("Delivery Note {0} created as Completed".format(delivery_note.name)), alert=True)

	def make_sale_invoice(self,order_items,debit_to,isum):
		sales_invoice = frappe.new_doc('Sales Invoice')
		sales_invoice.update({
			"customer": self.customer,
			"customer_name": self.customer_name,
			"company": self.company,
			"debit_to":debit_to,
			"is_pos": 0,
			"due_date":self.end_date,
			"price_list_currency":get_default_currency() or frappe.get_cached_value('Company',  company,  'default_currency'),
			"ignore_pricing_rule":0,
			"conversion_rate":1,
			"plc_conversion_rate":1,
			"total":isum,
			"net_total":isum,
			"base_total":isum,
			"base_net_total":isum,
			"base_grand_total":isum,
			"base_rounded_total":isum,
			"grand_total":isum,
			"rounded_total":isum,
			'items': order_items,
			"maintenance_order":self.name,
			'payment_schedule':[{
				'due_date': self.end_date,
				'payment_amount':isum
				}]
			})
		sales_invoice.customer = self.customer
		#sales_invoice.set_missing_values(for_validate = True) 
		#sales_invoice.flags.ignore_validate = True
		#sales_invoice.flags.ignore_mandatory = True 
		#sales_invoice.flags.ignore_validate_update_after_submit = True
		#sales_invoice.flags.ignore_links = True
		sales_invoice.insert(ignore_permissions=True)
		sales_invoice.submit()
		frappe.db.sql("update `tabMaintenance Order` set invoice='{0}' where name ='{1}' ".format(sales_invoice.name,self.name));
		self.invoice = sales_invoice.name
		frappe.db.commit()

		for i in order_items: 
			frappe.db.sql('update `tabSales Invoice Item` set delivery_note=%s where parent=%s',(self.delivery_note,sales_invoice.name))

		frappe.msgprint(_("Sales Invoice {0} created as paid".format(sales_invoice.name)), alert=True)

	def pay_order(self,paid,status="Completed"):
		self.create_payment_entry(paid)
		self.status = status
		
		frappe.db.sql("update `tabMaintenance Order` set status='{0}' where name ='{1}' ".format(status,self.name));

		item=frappe.get_doc("Maintenance Item",self.item_code)
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
				pay=frappe.get_list("Payment Entry",['paid_amount','name'],filters={'reference_no':order.name})
				for p in pay:
					pp=frappe.get_doc("Payment Entry",p.name)
					total_paid+=pp.paid_amount

			orders_C=frappe.get_list("Maintenance Order",['name'],filters={'item_code':item.name,'docstatus':1})
			item.total_orders=len(orders)
			item.completed_orders=len(orders_C)
			item.total_amount=total
			item.total_prepaid=prepaid
			item.total_paid=total_paid
			item.flags.ignore_permissions = True
			item.save()

	def create_payment_entry(self,paid, submit=True):
		bank_account = frappe.db.get_value("MRS Settings", None, "bank_account")
		isum= 0
		order_items= self.get_items()
		for i in order_items: 
			isum += i['amount']

		if not paid:
			to_pay_amount= isum
		else:
			to_pay_amount= paid
			if self.prepaid: to_pay_amount= paid + self.prepaid

		"""create entry"""
		frappe.flags.ignore_account_permission = True

		ref_doc = frappe.get_doc("Sales Invoice", self.invoice)

		party_account = ref_doc.debit_to

		party_account_currency = ref_doc.get("party_account_currency") or get_account_currency(party_account)

		bank_amount = to_pay_amount
		#if party_account_currency == ref_doc.company_currency and party_account_currency != self.currency:
		#	party_amount = ref_doc.base_grand_total
		#else:
		party_amount = to_pay_amount

		payment_entry = get_payment_entry("Sales Invoice", self.invoice,
			party_amount=party_amount, bank_account=bank_account, bank_amount=bank_amount)

		payment_entry.update({
			"reference_no": self.name,
			"reference_date": nowdate(),
			"maintenance_order":self.name,
			"remarks": "Payment Entry against {0} {1} via Payment Request {2}".format("Sales Invoice",
				self.invoice, self.name)
		})

		if payment_entry.difference_amount:
			company_details = get_company_defaults(ref_doc.company)

			payment_entry.append("deductions", {
				"account": company_details.exchange_gain_loss_account,
				"cost_center": company_details.cost_center,
				"amount": payment_entry.difference_amount
			})

		if submit:
			payment_entry.insert(ignore_permissions=True)
			payment_entry.submit()

			payment_schedule = frappe.get_doc('Payment Schedule',{'parent':self.invoice} )
			payment_schedule.invoice_portion=100
			payment_schedule.flags.ignore_validate_update_after_submit = True
			payment_schedule.save(ignore_permissions = True)
			frappe.db.commit()

			for i in order_items: 
				frappe.db.sql('update `tabDelivery Note Item` set billed_amt=%s where parent=%s',(i['amount'],self.delivery_note))

			frappe.db.sql('update `tabDelivery Note` set per_billed=%s, status="Completed" where name=%s',(100,self.delivery_note))

		frappe.msgprint(_("Payment Entry {0} created as paid".format(payment_entry.name)), alert=True)
		return payment_entry




	def make_payment_entry(self):
		isum= 0
		order_items= self.get_items()
		for i in order_items: 
			isum += i['amount']

		debit_to= self.check_auto_process() 
		if debit_to:
			payment_schedule = frappe.get_doc('Payment Schedule',{'parent':self.invoice} )
			payment_schedule.invoice_portion=100
			payment_schedule.flags.ignore_validate_update_after_submit = True
			payment_schedule.save(ignore_permissions = True)
			frappe.db.commit()

			for i in order_items: 
				frappe.db.sql('update `tabDelivery Note Item` set billed_amt=%s where parent=%s',(i['amount'],self.delivery_note))
				frappe.db.commit()


			frappe.db.sql('update `tabDelivery Note` set per_billed=%s and status="Completed" where name=%s',(100,self.delivery_note))
			frappe.db.commit()


			frappe.flags.ignore_account_permission = True
			payment_entry = frappe.new_doc('Payment Entry')
			payment_entry.update({
				"party_type":'Customer',
				"party":self.customer,
				"party_name": self.customer_name,
				"payment_type": 'Receive',
				"allocate_payment_amount":1,
				"paid_from": debit_to,
				"paid_to":'your-company - ADM',
				"paid_amount":isum, #self.prepaid,
				"base_paid_amount":isum,#self.prepaid,
				"base_total_allocated_amount":isum,
				"references": [{
					'reference_doctype':'Sales Invoice',
					'reference_name':self.invoice,
					'due_date':self.end_date,
					'total_amount':isum,
					'outstanding_amount':isum,
					'allocated_amount':isum
					}]
				})
			payment_entry.flags.ignore_validate = True
			payment_entry.flags.ignore_mandatory = True 
			payment_entry.insert(ignore_permissions=True)
			payment_entry.submit()







		
#	def __init__(self, *args, **kwargs):
#		super(MaintenanceOrder, self).__init__(*args, **kwargs)



@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None, ignore_permissions=False):
	def postprocess(source, target):
		set_missing_values(source, target)
		#Get the advance paid Journal Entries in Sales Invoice Advance
		target.set_advances()

	def set_missing_values(source, target):
		target.is_pos = 0
		target.ignore_pricing_rule = 1
		target.flags.ignore_permissions = True
		target.run_method("set_missing_values")
		#target.run_method("set_po_nos")
		target.run_method("calculate_taxes_and_totals")

		# set company address
		#target.update(get_company_address(target.company))
		#if target.company_address:
		#	target.update(get_fetch_values("Sales Invoice", 'company_address', target.company_address))

	def update_item(source, target, source_parent):
		target.amount = flt(source.amount) 
		target.base_amount = target.amount 
		target.qty = target.amount / flt(source.rate) if (source.rate) else source.qty

		item = frappe.db.get_value("Item", target.item_code, ["item_group", "selling_cost_center"], as_dict=1)
		#target.cost_center = frappe.db.get_value("Project", source_parent.project, "cost_center") \
		#	or item.selling_cost_center \
		#	or frappe.db.get_value("Item Group", item.item_group, "default_cost_center")

	doclist = get_mapped_doc("Maintenance Order", source_name, {
		"Maintenance Order": {
			"doctype": "Sales Invoice",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Maintenance Order Items": {
			"doctype": "Sales Invoice Item",
			"postprocess": update_item
		}
	}, target_doc, postprocess, ignore_permissions=ignore_permissions)

	return doclist


@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None, ignore_permissions=False):
	def postprocess(source, target):
		set_missing_values(source, target)
		#Get the advance paid Journal Entries in Sales Invoice Advance
		#target.set_advances()

	def set_missing_values(source, target):
		target.is_pos = 0
		target.ignore_pricing_rule = 1
		target.flags.ignore_permissions = True
		target.run_method("set_missing_values")
		#target.run_method("set_po_nos")
		#target.run_method("calculate_taxes_and_totals")

		# set company address
		#target.update(get_company_address(target.company))
		#if target.company_address:
		#	target.update(get_fetch_values("Sales Invoice", 'company_address', target.company_address))

	def update_item(source, target, source_parent):
		target.amount = flt(source.amount) 
		target.base_amount = target.amount 
		target.qty = target.amount / flt(source.rate) if (source.rate) else source.qty

		item = frappe.db.get_value("Item", target.item_code, ["item_group", "selling_cost_center"], as_dict=1)
		#target.cost_center = frappe.db.get_value("Project", source_parent.project, "cost_center") \
		#	or item.selling_cost_center \
		#	or frappe.db.get_value("Item Group", item.item_group, "default_cost_center")

	doclist = get_mapped_doc("Maintenance Order", source_name, {
		"Maintenance Order": {
			"doctype": "Delivery Note",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Maintenance Order Items": {
			"doctype": "Delivery Note Item",
			"postprocess": update_item
		}
	}, target_doc, postprocess, ignore_permissions=ignore_permissions)

	return doclist

@frappe.whitelist()
def get_dashboard(name):
	prepaid=0
	total=0
	total_paid=0
	oo=frappe.get_doc("Maintenance Order",name)
	prepaid=oo.prepaid
	if oo.total:
		total=oo.total
	if oo.invoice:
		sales_invoices=frappe.get_list("Payment Entry Reference",['parent'],filters={'reference_name':oo.invoice,'reference_doctype':"Sales Invoice"})

		if sales_invoices:

			for sales in sales_invoices:
				ss=frappe.get_doc("Payment Entry",sales.parent)
				total_paid+=ss.paid_amount
	else:
		total_paid=prepaid

	return {'total' : total,
		'prepaid' : prepaid,
		'total_paid':total_paid
		} 
