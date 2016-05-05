#!/usr/bin/python
import sys
import xml.etree.ElementTree as ET
from models import Crisis, Organization, Person

def listings (elem):
	"""
	Parses elem for href, embed, text, and raw text
	Stores each item above in a string
	Returns the string
	"""
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

def merge_common(elem, m):
	"""
	Parses tags under the "<Common>" tag
	Checks if data already exists
	If so, do a merge 
	else, import the model data
	Stores parsed data in given model, m
	"""
	cite = elem.find("Citations")
	link = elem.find("ExternalLinks")
	image = elem.find("Images")
	video = elem.find("Videos")
	maps = elem.find("Maps")
	feeds = elem.find("Feeds")
	summary = elem.find("Summary")
	if(cite != None):
		str_cite = m.citations.split('\n')
		list_citations = listings(cite).split('\n')
		listunion(str_cite, list_citations)
		m.citations = '\n'.join(str_cite)
	if(link != None):
		str_extLinks = m.extLinks.split('\n')
		list_extLinks = listings(link).split('\n')
		listunion(str_extLinks, list_extLinks)
		m.extLinks = '\n'.join(str_extLinks)
	if(image != None):
		str_images = m.images.split('\n')
		list_images = listings(image).split('\n')
		listunion(str_images, list_images)
		m.images = '\n'.join(str_images)
	if(video != None):
		str_videos = m.videos.split('\n')
		list_videos = listings(video).split('\n')
		listunion(str_videos, list_videos)
		m.videos = '\n'.join(str_videos)
	if(maps != None):
		str_maps = m.maps.split('\n')
		list_maps = listings(maps).split('\n')
		listunion(str_maps, list_maps)
		m.maps = '\n'.join(str_maps)
	if(feeds != None):
		str_feeds = m.feeds.split('\n')
		list_feeds = listings(feeds).split('\n')
		listunion(str_feeds, list_feeds)
		m.feeds = '\n'.join(str_feeds)
	if(summary != None and summary.text != None):
		m.summary = summary.text

def merge_crises(elem):
	"""
	Parses data from "<Crisis />" tags
	Checks if entry already exists
	If so, do a merge 
	else, import the model data
	Saves model to mysql database
	"""
	for c in elem:
		cri_filter_obj = Crisis.objects.filter(wcdb_id = c.get('ID'))
		if len(cri_filter_obj) != 0:
			crisis = cri_filter_obj[0]	#if crisis exists, use it
			crisis.name = c.get('Name')
		else:					#else make a new one
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
						if(len(cri_filter_obj.filter(people__wcdb_id__exact = p.get('ID'))) == 0):
							crisis.people.add(person)	#if person is not listed, add it
							break
		list_org = Organization.objects.all()
		organizations = c.find('Organizations')
		if (organizations != None):
			for o in organizations:
				for org in list_org:
					if (o.get('ID') == org.wcdb_id):
						if(len(cri_filter_obj.filter(organizations__wcdb_id__exact = o.get('ID'))) == 0):
							crisis.organizations.add(org)	#if org is not listed, add it
							break
		if (date != None):
			crisis.date = date.text
		if (time != None):
			crisis.date += " " + time.text
		if (kind != None):
			crisis.kind = kind.text
		if (locations != None):
			str_locations = crisis.locations.split('\n')
			list_locations = listings(locations).split('\n')
			listunion(str_locations, list_locations)
			crisis.locations = '\n'.join(str_locations)
		if (human != None):
			str_human = crisis.humanImpact.split('\n')
			list_human = listings(human).split('\n')
			listunion(str_human, list_human)
			crisis.humanImpact = '\n'.join(str_human)
		if (eco != None):
			str_eco = crisis.economicImpact.split('\n')
			list_eco = listings(eco).split('\n')
			listunion(str_eco, list_eco)
			crisis.economicImpact = '\n'.join(str_eco)
		if (resource != None):
			str_resource = crisis.resources.split('\n')
			list_resource = listings(resource).split('\n')
			listunion(str_resource, list_resource)
			crisis.resources = '\n'.join(str_resource)
		if (help != None):
			str_help = crisis.waysToHelp.split('\n')
			list_help = listings(help).split('\n')
			listunion(str_help, list_help)
			crisis.waysToHelp = '\n'.join(str_help)
		if (common != None):
			merge_common(common, crisis)
		crisis.save()

def merge_people(elem):
	"""
	Parses data from "<Person />" tags
	Checks if  entry already exists
	If so, do a merge 
	else, import the model data
	Saves model to mysql database
	"""
	for p in elem :
		person_filter_obj = Person.objects.filter(wcdb_id = p.get('ID'))
		if (len(person_filter_obj) != 0):
			person = person_filter_obj[0]	#if person exists, use it
			person.name = p.get('Name')
		else:					#else make a new one
			person = Person(name = p.get('Name'), wcdb_id = p.get('ID'))
		kind = p.find('Kind')
		location = p.find('Location')
		common = p.find('Common')
		if (kind != None): 
			person.kind = kind.text
		if (location != None):
			person.location = location.text
		if (common != None):
			merge_common(common, person)
		person.save()

def merge_organizations(elem):
	"""
	Parses data from "<Organization />" tags
	Stores in Django model
	Saves model to mysql database
	"""
	for o in elem :
		org_filter_obj = Organization.objects.filter(wcdb_id = o.get('ID'))
		if (len(org_filter_obj) != 0):
			org = org_filter_obj[0]	#if org exists, use it
			org.name = o.get('Name')
		else:				#else make a new one
			org = Organization(name = o.get('Name'), wcdb_id = o.get('ID'))
		people = o.find('People')
		org.save()
		list_people = Person.objects.all()
		if (people != None):
			for p in people:
				for person in list_people:
					if (p.get('ID') == person.wcdb_id):
						if(len(org_filter_obj.filter(people__wcdb_id__exact = p.get('ID'))) == 0):
							org.people.add(person)
							break
		kind = o.find('Kind')
		location = o.find('Location')
		hist = o.find('History')
		contact = o.find('ContactInfo')
		common = o.find('Common')
		if (kind != None):
			org.kind = kind.text
		if (location != None):
			org.location =  location.text
		if (hist != None):
			str_hist = org.history.split('\n')
			list_hist = listings(hist).split('\n')
			listunion(str_hist, list_hist)
			org.history = '\n'.join(str_hist)
		if (contact != None):
			str_contact = org.contact.split('\n')
			list_contact = listings(contact).split('\n')
			listunion(str_contact, list_contact)
			org.contact = '\n'.join(str_contact)
		if (common != None):
			merge_common(common, org)
		org.save()

def merge_m2mfields(people, orgs):
	for p in people:
		per_filter_obj = Person.objects.filter(wcdb_id = p.get('ID'))
		list_org = Organization.objects.all()
		organizations = p.find('Organizations')
		if (organizations != None):
			for o in organizations:
				for org in list_org:
					if (o.get('ID') == org.wcdb_id):
						if(len(per_filter_obj.filter(organization__wcdb_id__exact = o.get('ID'))) == 0):
							per_filter_obj[0].organization_set.add(org)	#if org is not listed, add it
							break
		list_cri = Crisis.objects.all()
		crises = p.find('Crises')
		if (crises != None):
			for c in crises:
				for cri in list_cri:
					if (c.get('ID') == cri.wcdb_id):
						if(len(per_filter_obj.filter(crisis__wcdb_id__exact = c.get('ID'))) == 0):
							per_filter_obj[0].crisis_set.add(cri)	#if org is not listed, add it
							break
	for o in orgs:
		org_filter_obj = Organization.objects.filter(wcdb_id = o.get('ID'))
		crises = o.find('Crises')
		if (crises != None):
			for c in crises:
				for cri in list_cri:
					if (c.get('ID') == cri.wcdb_id):
						if(len(per_filter_obj.filter(crisis__wcdb_id__exact = c.get('ID'))) == 0):
							org_filter_obj[0].crisis_set.add(cri)	#if org is not listed, add it
							break

def listunion(a,b):
	"""
	Combines list a and b
	Removes duplicates
	"""
	for i in b:
		if i not in a:
			a.append(i)

def merge_m2m_texts():
	list_people = Person.objects.all()
	list_org = Organization.objects.all()
	list_crisis = Crisis.objects.all()
	for c in list_crisis :
		current_ptext = c.people_text.split('\n')
		new_ptext = ''
		for p in c.people.all() :
			new_ptext += p.name + '\n'
		listunion(current_ptext, new_ptext.split('\n'))
		c.people_text = '\n'.join(current_ptext)

		current_otext = c.organizations_text.split('\n')
		new_otext = ''
		for o in c.organizations.all() :
			new_otext += o.name + '\n'
		listunion(current_otext, new_otext.split('\n'))
		c.organizations_text = '\n'.join(current_otext)
		c.save()


	for o in list_org :
		current_ptext = c.people_text.split('\n')
		new_ptext = ''
		for p in o.people.all() :
			new_ptext += p.name + '\n'
		listunion(current_ptext, new_ptext.split('\n'))
		o.people_text = '\n'.join(current_ptext)

		current_ctext = o.crisis_text.split('\n')
		new_ctext = ''
		for c in o.crisis_set.all() :
			new_ctext += c.name + '\n'
		listunion(current_ctext, new_ctext.split('\n'))
		o.crisis_text = '\n'.join(current_ctext)
		o.save()

	for p in list_people :
		current_otext = p.organizations_text.split('\n')
		new_otext = ''
		for o in p.organization_set.all() :
			new_otext += o.name + '\n'
		listunion(current_otext, new_otext)
		p.organizations_text = '\n'.join(current_otext)

		current_ctext = p.crisis_text.split('\n')
		new_ctext = ''
		for c in p.crisis_set.all() :
			new_ctext += c.name + '\n'
		listunion(current_ctext, new_ctext)
		p.crisis_text = '\n'.join(current_ctext)
		p.save()

def merge_xml(data):
	"""
	Creates root of XML from given data
	Runs all import functions on data
	"""
	assert data != None
	#put in some queries
	root = ET.fromstring(data)
	merge_people(root.findall('Person'))
	merge_organizations(root.findall('Organization'))
	merge_crises(root.findall('Crisis'))
	merge_m2mfields(root.findall('Person'), root.findall('Organization'))
	merge_m2m_texts()
