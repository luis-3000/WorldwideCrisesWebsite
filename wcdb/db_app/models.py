from django.db import models


class Person(models.Model):
	wcdb_id = models.CharField(max_length=10)
	name = models.TextField(blank=True)
	kind = models.TextField(blank=True)
	organizations_text = models.TextField(blank=True)
	crisis_text = models.TextField(blank=True)
	location = models.TextField(blank=True)
	citations = models.TextField(blank=True)
	extLinks = models.TextField(blank=True)
	images = models.TextField(blank=True)
	videos = models.TextField(blank=True)
	maps = models.TextField(blank=True)
	feeds = models.TextField(blank=True)
	summary = models.TextField(blank=True)

	def __unicode__(self):
		return self.name

class Organization(models.Model):
	wcdb_id = models.CharField(max_length=10)
	name = models.TextField(blank=True)
	people = models.ManyToManyField(Person, blank=True)
	people_text = models.TextField(blank=True)
	crisis_text = models.TextField(blank=True)
	kind = models.TextField(blank=True)
	location = models.TextField(blank=True)
	history = models.TextField(blank=True)
	contact = models.TextField(blank=True)
	citations = models.TextField(blank=True)
	extLinks = models.TextField(blank=True)
	images = models.TextField(blank=True)
	videos = models.TextField(blank=True)
	maps = models.TextField(blank=True)
	feeds = models.TextField(blank=True)
	summary = models.TextField(blank=True)

	def __unicode__(self):
		return self.name

class Crisis(models.Model):
	wcdb_id = models.CharField(max_length=10)
	name = models.TextField(blank=True)
	people = models.ManyToManyField(Person, blank=True)
	organizations = models.ManyToManyField(Organization, blank=True)
	people_text = models.TextField(blank=True)
	organizations_text = models.TextField(blank=True)
	kind = models.TextField(blank=True)
	date = models.DateTimeField(blank=True, null=True)
	locations = models.TextField(blank=True)
	humanImpact = models.TextField(blank=True)
	economicImpact = models.TextField(blank=True)
	resources = models.TextField(blank=True)
	waysToHelp = models.TextField(blank=True)
	citations = models.TextField(blank=True)
	extLinks = models.TextField(blank=True)
	images = models.TextField(blank=True)
	videos = models.TextField(blank=True)
	maps = models.TextField(blank=True)
	feeds = models.TextField(blank=True)
	summary = models.TextField(blank=True)

	# def __unicode__(self):
	# 	return self.name
