# -*- coding: utf-8 -*- 
from db_app.models import Crisis, Person, Organization
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.template import RequestContext, Context, loader
from forms import DocumentFormImport, DocumentFormMerge
from WebImportExport import import_xml, export_xml, merge_xml
from minixsv_v9.WebMiniXSV import check_imported_file
import xml.dom.minidom
from search import get_query
from itertools import chain
import re


# the context is a dictionary mapping template variable names to Python objects.


def index(request):
	"""
	renders homepage
	"""
	return render_to_response('index.html')

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
			form = DocumentFormImport(request.POST, request.FILES)
			if form.is_valid():
				imported_file = request.FILES['docfile'].read()
				try:
					filePassesSchema = check_imported_file(imported_file)
				except Exception:
					filePassesSchema = False
				if filePassesSchema:
					Crisis.objects.all().delete()		#clear database first
					Organization.objects.all().delete()
					Person.objects.all().delete()
					import_xml(imported_file)			#import
					return render_to_response('importing.html', {'status': 'Import succeeded.'})
				else:
					return render_to_response('importing.html', {'status': 'Import failed. File does not match schema.'})
		else:
			form = DocumentFormImport()
		return render_to_response('import.html', {'form': form, 'importf': True}, context_instance=RequestContext(request))
	else:
		return render_to_response('login.html', context_instance=RequestContext(request))

def web_merge_xml(request):
	"""
	redirects to login page if user is not logged in
	otherwise, renders page with import functionality
	if called with POST request...
		check imported data against schema using minixsv
		puts data into database if validation succeeds
	"""
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = DocumentFormMerge(request.POST, request.FILES)
			if form.is_valid():
				imported_file = request.FILES['docfile'].read()
				try:
					filePassesSchema = check_imported_file(imported_file)
				except Exception:
					filePassesSchema = False
				if filePassesSchema:
					merge_xml(imported_file)
					return render_to_response('importing.html', {'status': 'Merge succeeded.'})
				else:
					return render_to_response('importing.html', {'status': 'Merge failed. File does not match schema.'})
		else:
			form = DocumentFormMerge()
		return render_to_response('import.html', {'form': form, 'mergef': True}, context_instance=RequestContext(request))
	else:
		return render_to_response('login.html', context_instance=RequestContext(request))

def web_export_xml(request):
	"""
	renders export page
	"""
	return render_to_response('export.html')

def clear_database(request):
	"""
	clears the database if user is authenticated
	"""
	if request.user.is_authenticated():
		if request.method == 'POST':
			Crisis.objects.all().delete()		#clear database
			Organization.objects.all().delete()
			Person.objects.all().delete()
			return render_to_response('importing.html', {'status': 'Database has been cleared.'})
		else:
			return render_to_response('importing.html', {'status': 'Error: Database has not been cleared. Try again from the import page.'})			
	else:
		return render_to_response('login.html', context_instance=RequestContext(request))

def export_display(request):
	"""
	displays formatted xml export of database
	"""
	raw = export_xml()
	exported_data = xml.dom.minidom.parseString(raw).toprettyxml().replace('&quot;', '"')
	t = loader.get_template("export_display.html")
	c = RequestContext(request, {"exported_data" : raw})
	return HttpResponse((t.render(c)), content_type="text/xml")
	# return render_to_response('export.html', {'exported_data' : exported_data})

def export_download(request):
	"""
	prompts user to download an export file of entire database
	"""
	raw = export_xml()
	f_export = open('export_file.xml', 'w')
	f_export.write(raw)
	f_export.close()
	response = HttpResponse(FileWrapper(file('export_file.xml')), content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=export_file.xml'
	return response

def login(request):
	"""
	if user is not logged in...
		redirect to login page
	otherwise redirect to 'already logged in' page
	if called with POST request...
		attempt to log user in
		redirect to success or failure page
	"""
	redirect_to = request.REQUEST.get('next', '')
	if request.user.is_authenticated():
		return render_to_response("loggedin", {'login_status':'Already logged in.' })
	if request.method == 'POST':
		user = request.POST.get('user', '')
		passw = request.POST.get('pass', '')
		user = auth.authenticate(username=user, password=passw)
		if user is not None and user.is_active:
			auth.login(request, user)
			return render_to_response("loggedin")
			# return HttpResponseRedirect(redirect_to)
		else:
			return render_to_response("invalid")
	else:
		return render_to_response('login.html', context_instance=RequestContext(request))

def logout(request):
	"""
	if user is logged in...
		logs user out
		render logout success page
	else
		render 'not logged in' page
	"""
	redirect_to = request.REQUEST.get('next', '')
	if request.user.is_authenticated():
		auth.logout(request)
		return render_to_response('logout.html', {'msg':'You have been logged out.'})
	else:
		return render_to_response('logout.html', {'msg':'You are not currently logged in.'})

def search(request):
	query_string = ''
	found_entries = None
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']

		entry_query = get_query(query_string, ['name', 'kind', 'location', 'citations'])
		per_entries = Person.objects.filter(entry_query)

		entry_query = get_query(query_string, ['name', 'kind', 'location', 'history'])
		org_entries = Organization.objects.filter(entry_query)

		entry_query = get_query(query_string, ['name', 'kind', 'locations'])
		cri_entries = Crisis.objects.filter(entry_query)

		found_entries = list(chain(per_entries, org_entries, cri_entries))
	return render_to_response('search.html', { 'query_string': found_entries}, 
								context_instance=RequestContext(request))
