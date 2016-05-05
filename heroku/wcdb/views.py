from django.template import Context, RequestContext, Template, loader
from db_app.models import Crisis, Person, Organization
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
import random
import re

def index(request):
	t = loader.get_template("index.html")
	member_list = [	'Phillip Pham',
					'Justin Nguyen',
					'Alex Koontz',
					'Jose Castillo',
					'Austin Everts',
					'Spencer Mosley']
	member_list = randomly(member_list)
	context = RequestContext(request,
								 {'member_list' : member_list,
								  'billip'      : 'bobbit'}
								)
	return HttpResponse(t.render(context))
	
def randomly (lst):
	ret_lst = []
	while len(lst) > 0:
		rand_idx = random.randint(0, len(lst)-1)
		ret_lst.append(lst[rand_idx])
		lst.remove(lst[rand_idx])
	return ret_lst

def list_crises(request):
	"""
	renders list of crises from database 
	"""
	crises_list = Crisis.objects.all()
	return render_to_response('list_crises.html', {'crises_list': crises_list})

def list_people(request):
	"""
	renders list of people from database 
	"""
	people_list = Person.objects.all()
	return render_to_response('list_people.html', {'people_list': people_list})

def list_organizations(request):
	"""
	renders list of organizations from database 
	"""
	organization_list = Organization.objects.all()
	return render_to_response('list_organizations.html', {'organization_list': organization_list})

def info_crisis(request, crisis_id):
	"""
	renders info on a specific crisis from database
	crisis_id is the django id of requested item
	"""
	crisis = get_object_or_404(Crisis, id=crisis_id)
	related_people = crisis.people.all()
	related_orgs = crisis.organizations.all()
	c_imgs = crisis.images.split('\n')
	r_imgs = ""
	for l in c_imgs:
		embed = re.findall('\"[^\"]*\"', l)
		# print embed
		# raw = re.search('>([^<]*)<', l)
		if len(embed) > 0:
			r_imgs += '<embed src=' + embed[0] + ' width=550 height=400>'

	c_vids = crisis.videos.split('\n')
	r_vids = ""
	for l in c_vids:
		href = re.findall('\"[^\"]*\"', l)
		findytuser = re.search('user', l)
		if findytuser != None:
			if len(href) > 0:
				r_vids += '\n' + l + '\n'
				continue
		# print href
		# raw = re.search('>([^<]*)<', l)
		if len(href) > 0:
			r_vids += '<iframe width="560" height="315" src=' + href[0] + ' frameborder="0" allowfullscreen></iframe>'

	c_map = crisis.maps.split('\n')
	r_maps = ""
	for l in c_map:
		href = re.findall('\"[^\"]*\"', l)
		findgmap = re.search('maps.google', l)
		if findgmap is None:
			if len(href) > 0:
				r_maps += '<embed src=' + href[0] + ' width=550 height=400>'
				continue
		if len(href) > 0:
			r_maps += '<iframe width="550" height="500" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="' + href[0].replace('"', '') + '&amp;ie=UTF8&amp;ll=29.988872,-90.047283&amp;spn=0.12508,0.179785&amp;output=embed' + '"></iframe>'
	return render_to_response('info_crisis.html', {'maps': r_maps, 'vids': r_vids, 'imgs':r_imgs, 'crisis': crisis, 'r_people': related_people, 'r_orgs': related_orgs})

def info_person(request, person_id):
	"""
	renders info on a specific person from database
	person_id is the django id of requested item
	"""
	person = get_object_or_404(Person, id=person_id)
	related_crises = person.crisis_set.all()
	related_orgs = person.organization_set.all()
	p_imgs = person.images.split('\n')
	r_imgs = ""
	for l in p_imgs:
		embed = re.findall('\"[^\"]*\"', l)
		# print embed
		# raw = re.search('>([^<]*)<', l)
		if len(embed) > 0:
			r_imgs += '<embed src=' + embed[0] + ' width=550 height=400>'

	p_vids = person.videos.split('\n')
	r_vids = ""
	for l in p_vids:
		href = re.findall('\"[^\"]*\"', l)
		findytuser = re.search('user', l)
		if findytuser != None:
			if len(href) > 0:
				r_vids += '\n' + l + '\n'
				continue
		# print href
		# raw = re.search('>([^<]*)<', l)
		if len(href) > 0:
			r_vids += '<iframe width="560" height="315" src=' + href[0] + ' frameborder="0" allowfullscreen></iframe>'

	p_maps = person.maps.split('\n')
	r_maps = ""
	for l in p_maps:
		href = re.findall('\"[^\"]*\"', l)
		findgmap = re.search('maps.google', l)
		if findgmap is None:
			if len(href) > 0:
				r_maps += '<embed src=' + href[0] + ' width=550 height=400>'
				continue
		if len(href) > 0:
			r_maps += '<iframe width="550" height="500" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="' + href[0].replace('"', '') + '&amp;ie=UTF8&amp;ll=29.988872,-90.047283&amp;spn=0.12508,0.179785&amp;output=embed' + '"></iframe>'
	return render_to_response('info_person.html', {'maps': r_maps, 'vids': r_vids, 'imgs':r_imgs, 'person': person, 'r_orgs': related_orgs, 'r_crises': related_crises})

def info_organization(request, organization_id):
	"""
	renders info on a specific organization from database
	organization_id is the django id of requested item
	"""
	organization = get_object_or_404(Organization, id=organization_id)
	related_crises = organization.crisis_set.all()
	related_people = organization.people.all()

	o_imgs = organization.images.split('\n')
	r_imgs = ""
	for l in o_imgs:
		embed = re.findall('\"[^\"]*\"', l)
		# print embed
		# raw = re.search('>([^<]*)<', l)
		if len(embed) > 0:
			r_imgs += '<embed src=' + embed[0] + ' width=550 height=400>'

	o_vids = organization.videos.split('\n')
	r_vids = ""
	for l in o_vids:
		href = re.findall('\"[^\"]*\"', l)
		findytuser = re.search('user', l)
		if findytuser != None:
			if len(href) > 0:
				r_vids += '\n' + l + '\n'
				continue
		# print href
		# raw = re.search('>([^<]*)<', l)
		if len(href) > 0:
			r_vids += '<iframe width="560" height="315" src=' + href[0] + ' frameborder="0" allowfullscreen></iframe>'

	o_map = organization.maps.split('\n')
	r_maps = ""
	for l in o_map:
		href = re.findall('\"[^\"]*\"', l)
		findgmap = re.search('maps.google', l)
		if findgmap is None:
			if len(href) > 0:
				r_maps += '<embed src=' + href[0] + ' width=550 height=400>'
				continue
		if len(href) > 0:
			r_maps += '<iframe width="550" height="500" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="' + href[0].replace('"', '') + '&amp;ie=UTF8&amp;ll=29.988872,-90.047283&amp;spn=0.12508,0.179785&amp;output=embed' + '"></iframe>'
	return render_to_response('info_organization.html', {'maps': r_maps, 'vids': r_vids, 'imgs':r_imgs, 'org': organization, 'r_crises': related_crises, 'r_people': related_people })

def web_import_xml(request):
	"""
	redirects to login page if user is not logged in
	otherwise, renders page with import functionality
	if called with POST request...
		check imported data against schema using minixsv
		puts data into database if validation succeeds
	"""
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = DocumentForm(request.POST, request.FILES)
			if form.is_valid():
				imported_file = request.FILES['docfile'].read()
				f_import = open('importXML.xml', 'w')
				f_import.write(imported_file)
				f_import.close()
				try:
					bo = check_imported_file(imported_file)
				except Exception:
					bo = False
				if bo:
					import_xml(imported_file)
					return render_to_response('importing.html', {'import_status': 'Import succeeded.'})
				else:
					return render_to_response('importing.html', {'import_status': 'Import failed.'})
		else:
			form = DocumentForm()
		return render_to_response('import.html', {'form': form}, context_instance=RequestContext(request))
	else:
		return render_to_response('login.html', context_instance=RequestContext(request))
		
