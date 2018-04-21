from django import forms
from hvz.main.models import Player
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
#from django_localflavor_us.forms import USPhoneNumberField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django import forms

class MailerForm(forms.Form):

	ALLPLAYERS = "All"
	HUMANS = "Humans"
	ZOMBIES = "Zombies"
	
	KindCHOICES = [
		(ALLPLAYERS, "All Players"),
		(HUMANS, "Humans"),
		(ZOMBIES, "Zombies")]

	SchoolCHOICES = [
		('Mudd', 'Mudd'),
		('CMC', 'CMC'),
		('Pitzer', 'Pitzer'),
		('Pomona', 'Pomona'),
		('Scripps', 'Scripps')]

	sender = "hvzwattest@gmail.com"
	# sender = "mod@claremonthvz.org"

	#Email Field validates that the given value is a valid email address
	
	# Dropdown menu of team filters
	recipient = forms.ChoiceField(
		label=_("To:"),
		required=True, 
		choices = KindCHOICES
		)

	# checkboxes of school filtering options
	school = forms.MultipleChoiceField(
		choices = SchoolCHOICES,
		widget = forms.CheckboxSelectMultiple(),
		required = False)
	
	# subject line text field (aligned with body text)
	subject = forms.CharField(
		label=_("Subject:"),
		required=True,
		widget=forms.Textarea(attrs={'cols': '97', 'rows': 1})
		)

	# body text field
	body = forms.CharField(
		label=_("Body:"),
		required=False,
		widget=forms.Textarea(attrs={'cols': '100', 'rows': 10})
		)

	# attachment button
	attachment = forms.FileField(
		label= ("Attachment:"),
		required=False
		)

