#!/usr/bin/python
import sys
import xml.etree.ElementTree as ET
from models import Crisis, Organization, Person

def listings (elem):
	"""
	Parses elem for href, embed, text, and raw text
	Stores each item above in a dictionary
	Returns the dictionary
	"""
	assert elem != None
	a = ""
	for child in elem:
		href = child.get('href')
		embed = child.get('embed')
		text = child.get('text')
		raw = child.text
		if(href != None):
			a += '<a href="' + str(href) + '">'
			if(raw != None):
				a += str(raw)
			a += '</a>\n'
			continue
		elif(embed != None):
			a += '<embed src="' + str(embed) + '" '
			if(text != None):
				a += 'text="' + str(text) + '"'
			a += '>\n'
			continue
		elif(raw != None):
			a += str(raw) + '\n'
	return a

def make_common(elem, m):
	"""
	Parses tags under the "<Common>" tag
	Stores parsed data in given model, m
	"""
	assert elem != None
	cite = elem.find("Citations")
	link = elem.find("ExternalLinks")
	image = elem.find("Images")
	video = elem.find("Videos")
	maps = elem.find("Maps")
	feeds = elem.find("Feeds")
	summary = elem.find("Summary")
	if(cite != None):
		m.citations += listings(cite)
	if(link != None):
		m.extLinks += listings(link)
	if(image != None):
		m.images += listings(image)
	if(video != None):
		m.videos += listings(video)
	if(maps != None):
		m.maps += listings(maps)
	if(feeds != None):
		m.feeds += listings(feeds)
	if(summary != None and summary.text != None):
		m.summary += summary.text

def eval_crises(elem):
	"""
	Parses data from "<Crisis />" tags
	Stores in Django model
	Saves model to mysql database
	"""
	for c in elem:
		assert c.get('ID') != None
		assert c.get('Name') != None
		crisis = Crisis(name = c.get('Name'), wcdb_id = c.get('ID'))
		date = c.find('Date')
		people = c.find('People')
		kind = c.find('Kind')
		time = c.find('Time')
		locations = c.find('Locations')
		human = c.find('HumanImpact')
		eco = c.find('EconomicImpact')
		resource = c.find('ResourcesNeeded')
		help = c.find('WaysToHelp')
		common = c.find('Common')
		crisis.save()	#need to save model before m2m can be used
		list_people = Person.objects.all()
		if (people != None):
			for p in people:
				for person in list_people:
					if (p.get('ID') == person.wcdb_id):
						crisis.people.add(person)
						break
		list_org = Organization.objects.all()
		organizations = c.find('Organizations')
		if (organizations != None):
			for o in organizations:
				for org in list_org:
					if (o.get('ID') == org.wcdb_id):
						crisis.organizations.add(org)
						break
		if(date != None):
			crisis.date = date.text
		if(time != None):
			crisis.date += " " + time.text
		if(kind != None):
			crisis.kind = kind.text
		if(locations != None):
			crisis.locations += listings(locations)
		if(human != None):
			crisis.humanImpact += listings(human)
		if(eco != None):
			crisis.economicImpact += listings(eco)
		if(resource != None):
			crisis.resources += listings(resource)
		if(help != None):
			crisis.waysToHelp += listings(help)
		if(common != None):
			make_common(common, crisis)
		crisis.save()

def eval_people(elem):
	"""
	Parses data from "<Person />" tags
	Stores in Django model
	Saves model to mysql database
	"""
	for p in elem :
		assert p.get('ID') != None
		assert p.get('Name') != None
		person = Person(name = p.get('Name'), wcdb_id = p.get('ID'))
		kind = p.find('Kind')
		location = p.find('Location')
		common = p.find('Common')
		if(kind != None): 
			person.kind = kind.text
		if(location != None):
			person.location = location.text
		if(common != None):
			make_common(common, person)
		person.save()

def eval_organizations(elem):
	"""
	Parses data from "<Organization />" tags
	Stores in Django model
	Saves model to mysql database
	"""
	for o in elem :
		assert o.get('ID') != None
		assert o.get('Name') != None
		org = Organization(name = o.get('Name'), wcdb_id = o.get('ID'))
		people = o.find('People')
		org.save()
		list_people = Person.objects.all()
		if (people != None):
			for p in people:
				for person in list_people:
					if (p.get('ID') == person.wcdb_id):
						org.people.add(person)
						break
		kind = o.find('Kind')
		location = o.find('Location')
		hist = o.find('History')
		contact = o.find('ContactInfo')
		common = o.find('Common')
		if(kind != None):
			org.kind = kind.text
		if(location != None):
			org.location =  location.text
		if(hist != None):
				org.history += listings(hist)
		if(contact != None):
				org.contact += listings(contact)
		if(common != None):
			make_common(common, org)
		org.save()

def fill_texts():
	list_people = Person.objects.all()
	list_org = Organization.objects.all()
	list_crisis = Crisis.objects.all()
	for c in list_crisis :
		for p in c.people.all() :
			c.people_text += p.name + "\n"
		for o in c.organizations.all() :
			c.organizations_text += o.name + "\n"
		c.save()

	for o in list_org :
		for p in o.people.all() :
			o.people_text += p.name + "\n"
		for c in list_crisis :
			if o.name in c.organizations_text :
				o.crisis_text += c.name + "\n"
		o.save()

	for p in list_people :
		for o in list_org :
			if p.name in o.people_text :
				p.organizations_text += o.name + "\n"
		for c in list_crisis :
			if p.name in c.people_text :
				p.crisis_text += c.name + "\n"
		p.save()

def import_xml_solve(data):
	"""
	Creates root of XML from given data
	Runs all import functions on data
	"""
	assert data != None
	root = ET.fromstring(data)
	eval_people(root.findall('Person'))
	eval_organizations(root.findall('Organization'))
	eval_crises(root.findall('Crisis'))
	fill_texts()