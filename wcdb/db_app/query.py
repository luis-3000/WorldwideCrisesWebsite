#!/usr/bin/python
import sys
import datetime
from db_app.models import Crisis, Organization, Person

#returns objects
def people_with_most_images ():
	people = []
	num = -1
	for p in Person.objects.all() :
		count = p.images.count('\n')
		if count > num :
			people = []
			people.append(p)
			num = count
		elif num == count :
			people.append(p)
	return people

#returns objects
def ND_assocated_with_most_organizations ():
	crisis = []
	num = -1
	for c in Crisis.objects.all():
		count = c.organizations_text.count('\n')
		if count > num :
			crisis = []
			crisis.append(c)
			num = count 
		elif count == num :
			crisis.append(c)
	return crisis

#returns objects
def two_thousand_five_to_2010_crisis ():
	return Crisis.objects.all().filter(date__gte='2005-01-01', date__lte='2010-12-31')

#returns list [recources, ways to help]
def ways_to_help_resources_crisis_lt_2_orgs ():
	resources = []
	ways_to_help = []
	for c in Crisis.objects.all():
		count = c.organizations_text.count('\n')
		if count < 2 :
			resources.append(str(c.resources))
			ways_to_help.append(str(c.waysToHelp) )
	retval = []
	retval.append(resources)
	retval.append(ways_to_help)
	return retval

#returns list [locations, maps]
def loc_map_crisis ():
	locs = []
	maps = []
	for c in Crisis.objects.all():
		locs.append(str(c.locations))
		maps.append(str(c.maps))
	retval = []
	retval.append(locs)
	retval.append(maps)
	return retval

#returns objects
def alpha_crisis ():
	return Crisis.objects.order_by('name')

#returns in (number of images)
def num_images_since_2000 ():
	cris = Crisis.objects.all().filter(date__gte='2000-01-01')
	images = 0
	for c in cris :
		images += c.images.count('\n')
	return images

#returns list [names, economic impact]
def name_eco_ND_after_2001 ():
	names = []
	eco = []
	cris = Crisis.objects.all().filter(date__gte='2001-01-01')
	for c in cris :
		names.append(c.name)
		eco.append(c.economicImpact)
	retval = []
	retval.append(names)
	retval.append(eco)
	return retval

#returns list [names, types, locs]
def name_type_location_orgs ():
	names = []
	types = []
	locs = []
	for o in Organization.objects.all() :
		names.append(o.name)
		types.append(o.kind)
		locs.append(o.location)
	retval = []
	retval.append(names)
	retval.append(types)
	retval.append(locs)
	return retval
	
#returns list [ids, contact]
def id_contact_orgs_with_multiple_crisis ():
	count = 0
	ids = []
	contact = []
	for o in Organization.objects.all():
		count = o.crisis_text.count('\n')
		if count > 1 :
			ids.append(o.wcdb_id)
			contact.append(o.contact)
	retval = []
	retval.append(ids)
	retval.append(contact)
	return retval

#people_with_most_images()
#ND_assocated_with_most_organizations()
#two_thousand_five_to_2010_crisis()
#ways_to_help_resources_crisis_lt_2_orgs()
#loc_map_crisis()
#alpha_crisis()
#name_eco_ND_after_2001()
#name_type_location_orgs()
#id_contact_orgs_with_multiple_crisis()
num_images_since_2000()