# -*- coding: utf-8 -*- 
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from db_app.models import Crisis, Person, Organization
from WebImportExport import import_xml, export_xml
from WebMiniXSV import check_imported_file
from django.contrib import auth
from forms import DocumentForm
import xml.dom.minidom
import re


# the context is a dictionary mapping template variable names to Python objects.
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

def web_export_xml(request):
	"""
	renders export page
	"""
	return render_to_response('export.html')


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

