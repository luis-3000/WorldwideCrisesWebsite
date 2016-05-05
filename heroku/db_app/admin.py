from db_app.models import Crisis
from db_app.models import Organization
from db_app.models import Person
from django.contrib import admin

class CrisisAdmin(admin.ModelAdmin):
	list_display = ('name', 'kind', 'date')
	search_fields = ['name', 'kind', 'locations', 'people', 'organizations']
	# inlines = [CommonInline]

class OrgAdmin(admin.ModelAdmin):
	list_display = ('name', 'kind',)
	search_fields = ['name', 'kind', 'people', 'organizations']

class PersonAdmin(admin.ModelAdmin):
	list_display = ('name', 'kind',)
	search_fields = ['name', 'kind']

admin.site.register(Crisis, CrisisAdmin)
admin.site.register(Organization, OrgAdmin)
admin.site.register(Person, PersonAdmin)