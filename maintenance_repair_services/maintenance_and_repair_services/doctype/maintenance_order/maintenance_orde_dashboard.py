from frappe import _

def get_data():
	return {
		'heatmap': True,
		'heatmap_message': _('This is based on stock movement. See {0} for details')\
			.format('<a href="#query-report/Stock Ledger">' + _('Stock Ledger') + '</a>'),
		'fieldname': 'maintenance_order',
		'transactions': [

			{
				'label': _('Maintenance'),
				'items': ['Delivery Note', 'Sales Invoice']
			},
			{
				'label': _('Feedback'),
				'items': ['Customers Feedback', 'Expiry Dates Warning', 'Maintenance Stuff']
			}
		]
	}
