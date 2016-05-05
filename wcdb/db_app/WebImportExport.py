#!/usr/bin/env python
"""
Contains two functions.
Called from views.py to import/export data to/from django models
"""

# -------
# imports
# -------

from db_app.models import Crisis, Organization, Person
from importXML import import_xml_solve
from exportXML import export_xml_solve
from mergeXML import merge_xml as mxml

# ----
# main
# ----



def import_xml(data):
	"""
	Imports given data into mysql database
	"""
	import_xml_solve(data)

def export_xml():
	"""
	Exports mysql database into XML document
	"""
	return export_xml_solve(Crisis, Organization, Person)

def merge_xml(data):
	"""
	Merges import data with database
	"""
	mxml(data)