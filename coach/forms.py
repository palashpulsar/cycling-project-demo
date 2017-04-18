from django import forms

class gpx_file_form(forms.Form):
	docfile = forms.FileField(label='Select a GPX file')