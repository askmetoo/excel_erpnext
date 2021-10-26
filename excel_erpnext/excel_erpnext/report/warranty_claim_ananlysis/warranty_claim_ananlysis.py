# Copyright (c) 2013, Castlecraft Ecommerce Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import requests
import json

def execute(filters=None):
	api_key = frappe.get_conf().get("encryption_key")
	
	columns = get_columns(filters)
	data = get_result(filters)
	
	return columns, data

def get_columns(filters):

	columns = [
		{"label": ("Claim Date"), "fieldname": "claim_date", "fieldtype": "data","width": 100},
		{"label": ("Customer"), "fieldname": "customer", "fieldtype": "data","width": 100},
		{"label": ("Item Name"), "fieldname": "item_name", "fieldtype": "data","width": 100},
		{"label": ("Serial No"), "fieldname": "serial_no", "fieldtype": "data","width": 100},
		{"label": ("Sale Price"), "fieldname": "sale_price", "fieldtype": "data","width": 100},
		{"label": ("Claim No"), "fieldname": "claim_no", "fieldtype": "data","width": 100},
		{"label": ("Claim Type"), "fieldname": "claim_type", "fieldtype": "data","width": 100},
		{"label": ("Claim Status"), "fieldname": "claim_status", "fieldtype": "data","width": 100},
		{"label": ("RMA Status"), "fieldname": "rma_status", "fieldtype": "data","width": 100},
		{"label": ("RMA Verdict"), "fieldname": "rma_verdict", "fieldtype": "data","width": 100},
		{"label": ("Replace Serial"), "fieldname": "replace_serial", "fieldtype": "data","width": 100},
		{"label": ("Replace Product"), "fieldname": "replace_product", "fieldtype": "data","width": 100},
		{"label": ("Service Invoice Amount"), "fieldname": "service_invoice_amount", "fieldtype": "data","width": 100},
		{"label": ("Delivery Date"), "fieldname": "delivery_date", "fieldtype": "data","width": 100},
	]

	return columns
def get_result(filters):
	customer = frappe.db.get_value('Customer', {"name":filters.get("customer")}, ['customer_name'])
	params = {
		"fromDate":filters.get("from_date"),
		"toDate":filters.get("to_date"),
		"territory":filters.get("territory"),
		"item_name":filters.get("claim_item"),
		"claim_type":filters.get("claim_type"),
		"product_brand":filters.get("brand"),
		"claim_status":filters.get("claim_status"),
		"replace_item":filters.get("replaced_item"),
		"delivery_status":filters.get("delivery_status"),
		"customer":customer,
		"third_party_name":filters.get("third_party_name"),
		"thrid_party_mobile":filters.get("thrid_party_mobile"),
	}
	url = "http://testrma.excelbd.com/api/warranty_claim_analysis/v1/list"
	headers = {"x-frappe-api-key": frappe.get_conf().get("x-frappe-api-key")}
	if not frappe.get_conf().get("x-frappe-api-key"):
		frappe.throw("x-frappe-api-key is Not in Headers")
	response = requests.get(url,headers=headers,params=params)
	docs = json.loads(response.text)
	res = []
	for i in docs.get("docs"):
		sale_price = frappe.db.get_value('Item Price', {"price_list":filters.get("price_list"),"item_name":i.get("item_name"),"item_code":i.get("item_code")}, ['price_list_rate'])
		verdict = i.get("status_history")[-1].get("verdict")
		delivery_status = i.get("status_history")[-1].get("delivery_status")
		entry = {
			"claim_date":i.get("warranty_claim_date"),
			"customer":i.get("customer"),
			"item_name":i.get("item_name"),
			"serial_no":i.get("serial_no"),
			"sale_price":sale_price,
			"claim_no":i.get("claim_no"),
			"claim_type":i.get("claim_type"),
			"claim_status":i.get("claim_status"),
			"rma_status":verdict,
			"rma_verdict":delivery_status,
			"replace_serial":i.get("replace_serial"),
			"replace_product":i.get("replace_product"),
			"service_invoice_amount":i.get("billed_amount"),
			"delivery_date":i.get("delivery_date")
		}
		res.append(entry)
	return res
	