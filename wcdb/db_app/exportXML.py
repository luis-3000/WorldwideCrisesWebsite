#!/usr/bin/python
import sys
import ast
import re
import xml.etree.ElementTree as ET
from db_app.models import Crisis, Organization, Person

def eval_links(str_field, node, common):
	"""
	str_field is an array of strings
	node is the ElementTree object being constructed
	common is the <Common> XML tag being constructed
	Parses dictionary into <li> objects
	Appends <li> objects to node
	Appends node to common
	"""
	if (len(str_field) == 1) and (str_field[0] == ''):
		return
	for l in str_field:
		if l != '':
			li = ET.fromstring('<li />')
			href = re.search('href', l)
			embed = re.search('embed', l)
			text = re.search('text', l)
			acontents = re.findall('\"[^\"]*\"', l)
			raw = re.search('>([^<]*)<', l)
			if href != None:
				li.set('href', acontents[0].replace('"', ''))
				if raw != None:
					li.text = (raw.group(1))
			elif embed != None:
				li.set('embed', acontents[0].replace('"', ''))
				if text != None:
					li.set('text', acontents[1].replace('"', ''))
			else:
				li.text = l
			node.append(li)
	common.append(node)
	
def eval_common(m, main):
	"""
	m is a Django model
	main is the XML tree being constructed
	Parses data from all three models
	Stores data in an ElementTree object
	Appends those objects to main
	"""
	common = ET.fromstring('<Common />')
	citations = ET.fromstring('<Citations />')
	extLinks = ET.fromstring('<ExternalLinks />')
	images = ET.fromstring('<Images />')
	videos = ET.fromstring('<Videos />')
	maps = ET.fromstring('<Maps />')
	feeds = ET.fromstring('<Feeds />')
	summary = ET.fromstring('<Summary />')
	str_citations = str(m.citations).split('\n')
	str_extLinks = str(m.extLinks).split('\n')
	str_images = str(m.images).split('\n')
	str_videos = str(m.videos).split('\n')
	str_maps = str(m.maps).split('\n')
	str_feeds = str(m.feeds).split('\n')
	eval_links(str_citations, citations, common)
	eval_links(str_extLinks, extLinks, common)
	eval_links(str_images, images, common)
	eval_links(str_videos, videos, common)
	eval_links(str_maps, maps, common)
	eval_links(str_feeds, feeds, common)
	summary.text = m.summary
	if summary.text != '':
		common.append(summary)
	if len(common) != 0:
		main.append(common)

def eval_crises(crisis, root):
	"""
	crisis is the Crisis Django model
	Creates ElementTree object named child, which represents a Crisis model
	Parses data from Crisis models
	Stores data in ElementTree objects
	Appends objects to child
	Append child to root
	"""
	for c in crisis.objects.all():
		assert c.wcdb_id != None
		assert c.name != None
		child = ET.fromstring('<Crisis ID="' + c.wcdb_id + '" Name="' + c.name + '" />')
		people = ET.fromstring('<People />')
		for p in c.people.all():
			person = ET.fromstring('<Person ID="'+ p.wcdb_id + '" />')
			people.append(person)
		organizations = ET.fromstring('<Organizations />')
		for o in c.organizations.all():
			org = ET.fromstring('<Org ID="' + o.wcdb_id + '" />')
			organizations.append(org)
		kind = ET.fromstring('<Kind />')
		date = ET.fromstring('<Date />')
		time = ET.fromstring('<Time />')
		str_date = str(c.date).split()
		kind.text = c.kind
		date.text = str_date[0]
		time.text = str_date[1]
		locations = ET.fromstring('<Locations />')
		humanImpact = ET.fromstring('<HumanImpact />')
		economicImpact = ET.fromstring('<EconomicImpact />')
		resources = ET.fromstring('<ResourcesNeeded />')
		waysToHelp = ET.fromstring('<WaysToHelp />')
		common = ET.fromstring('<Common />')
		str_locations = str(c.locations).split('\n')
		str_humanImpact = str(c.humanImpact).split('\n')
		str_economicImpact = str(c.economicImpact).split('\n')
		str_resources = str(c.resources).split('\n')
		str_waysToHelp = str(c.waysToHelp).split('\n')
		root.append(child)
		if len(people) != 0:
			child.append(people)
		if len(organizations) != 0:
			child.append(organizations)
		if kind.text !="":
			child.append(kind)
		child.append(date)
		child.append(time)
		eval_links(str_locations, locations, child)
		eval_links(str_humanImpact, humanImpact, child)
		eval_links(str_economicImpact, economicImpact, child)
		eval_links(str_resources, resources, child)
		eval_links(str_waysToHelp, waysToHelp, child)
		eval_common(c, child)

def eval_organizations(org, root):
	"""
	org is the Organization Django model
	Creates ElementTree object named child, which represents an Organization model
	Parses data from Organization models
	Stores data in ElementTree objects
	Appends objects to child
	Append child to root
	"""
	for o in org.objects.all():
		assert o.wcdb_id != None
		assert o.name != None
		child = ET.fromstring('<Organization ID="' + o.wcdb_id + '" Name="' + o.name + '" />')
		crises = ET.fromstring('<Crises />')
		people = ET.fromstring('<People />')
		kind = ET.fromstring('<Kind />')
		location = ET.fromstring('<Location />')
		history = ET.fromstring('<History />')
		contact = ET.fromstring('<ContactInfo />')
		for c in o.crisis_set.all():
			crisis = ET.fromstring('<Crisis ID="' + c.wcdb_id + '" />')
			crises.append(crisis)
		for p in o.people.all():
			person = ET.fromstring('<Person ID="'+ p.wcdb_id + '" />')
			people.append(person)
		str_history = str(o.history).split('\n')
		str_contact = str(o.contact).split('\n')
		kind.text = o.kind
		location.text = o.location
		root.append(child)
		if len(crises) != 0:
			child.append(crises)
		if len(people) != 0:
			child.append(people)
		if location.text !="":
			child.append(location)
		eval_links(str_history, history, child)
		eval_links(str_contact, contact, child)
		eval_common(o, child)

def eval_people(people, root):
	"""
	people is the Person Django model
	Creates ElementTree object named child, which represents a Person model
	Parses data from Person model
	Stores data in ElementTree objects
	Appends objects to child
	Append child to root
	"""
	for p in people.objects.all():
		assert p.wcdb_id != None
		assert p.name != None
		child = ET.fromstring('<Person ID="' + p.wcdb_id + '" Name="' + p.name + '" />')
		crises = ET.fromstring('<Crises />')
		kind = ET.fromstring('<Kind />')
		location = ET.fromstring('<Location />')
		organizations = ET.fromstring('<Organizations />')
		for c in p.crisis_set.all():
			crisis = ET.fromstring('<Crisis ID="' + c.wcdb_id + '" />')
			crises.append(crisis)
		for o in p.organization_set.all():
			org = ET.fromstring('<Org ID="'+ o.wcdb_id + '" />')
			organizations.append(org)
		kind.text = p.kind
		location.text = p.location
		root.append(child)
		if len(crises) != 0:
			child.append(crises)
		if len(organizations) != 0:
			child.append(organizations)
		if kind.text != "":
			child.append(kind)
		if location.text !="":
			child.append(location)
		eval_common(p, child)

def export_xml_solve (c, o, p):
	"""
	c is the Crisis Django model
	o is the Organization Django model
	p is the Person Django model
	Creates ElementTree object root
	Runs all export functions
	Returns results of export as a string
	"""
	root = ET.fromstring('<WorldCrises></WorldCrises>') 
	eval_crises(c, root)
	eval_people(p, root)
	eval_organizations(o, root)
	assert root != None
	return ET.tostring(root)