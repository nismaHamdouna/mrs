# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "maintenance_repair_services"
app_title = "Maintenance and Repair Services"
app_publisher = "Maintenance and Repair Services"
app_description = "Maintenance and Repair Services"
app_icon = "octicon octicon-circuit-board"
app_color = "#00BCD4"
app_email = "Maintenance and Repair Services"
app_license = "MRS"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/maintenance_repair_services/css/maintenance_repair_services.css"
# app_include_js = "/assets/maintenance_repair_services/js/maintenance_repair_services.js"

# include js, css files in header of web template
# web_include_css = "/assets/maintenance_repair_services/css/maintenance_repair_services.css"
# web_include_js = "/assets/maintenance_repair_services/js/maintenance_repair_services.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "maintenance_repair_services.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "maintenance_repair_services.install.before_install"
after_install = "maintenance_repair_services.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

#notification_config = "maintenance_repair_services.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
fixtures = ["Custom Field"]
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"maintenance_repair_services.tasks.all"
# 	],
# 	"daily": [
# 		"maintenance_repair_services.tasks.daily"
# 	],
# 	"hourly": [
# 		"maintenance_repair_services.tasks.hourly"
# 	],
# 	"weekly": [
# 		"maintenance_repair_services.tasks.weekly"
# 	]
# 	"monthly": [
# 		"maintenance_repair_services.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "maintenance_repair_services.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "maintenance_repair_services.event.get_events"
# }

