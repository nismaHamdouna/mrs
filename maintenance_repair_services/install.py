# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os, json, sys, subprocess, shutil
import frappe
import frappe.database
import getpass
import importlib
from frappe import _
from frappe.model.db_schema import DbManager
from frappe.model.sync import sync_for
from frappe.utils.fixtures import sync_fixtures
from frappe.website import render
from frappe.desk.doctype.desktop_icon.desktop_icon import sync_from_app
from frappe.utils.password import create_auth_table
from frappe.utils.global_search import setup_global_search_table
from frappe.modules.utils import sync_customizations

def after_install():
	frappe.get_doc({"doctype" : "Item Category","product_category":"Item","active" : 1}).insert(ignore_permissions=True)

