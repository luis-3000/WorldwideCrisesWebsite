# -*- coding: utf-8 -*-
from django import forms

class DocumentFormImport(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )

class DocumentFormMerge(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )