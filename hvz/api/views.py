# file for code review
import json

from django.http import HttpResponse

from hvz.main.models import Player
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from hvz.api.forms import MailerForm
from django.shortcuts import render
from hvz.api import views
from django.urls import reverse


# List of emails and passwords to send from
# Allows users to bypass gmail's daily sending limit by sending from multiple accounts
EMAIL_LIST = ["hvzwattest@gmail.com", "hvzwattest2@gmail.com", "hvzwattest3@gmail.com", "hvzwattest4@gmail.com"]
EMAIL_PW_LIST = ["claremonthvz", "claremonthvz2", "claremonthvz3", "claremonthvz4"]

def json_get_all_emails(request):
    """A function that returns a list of strings representing player emails.
    Note that these emails are only those of players in the current game.
    """

    # Check out HVZ/main/models.py for helper functions relating to Players.
    # Player.current_players() returns all Players in the current Game.
    
    emails = [p.user.email for p in Player.current_players()]
    format = ",".join(emails)

    # json.dumps creates a string from a Python object. You can then
    # read the string and convert it into an Objective-C data
    # structure using NSJSONSerialization in Objective-C.
    json_data = json.dumps(format)

    return HttpResponse(
        json_data,
        content_type="application/json"
    )

def success(request):
    return render(request, 'api/success.html', {})

class Mailer(FormView):
    form_class = MailerForm
    template_name = "api/mailer.html"

    # return url
    success_url = 'successmailer'

    def dispatch(self, *args, **kwargs):
        # used to display the form
        return super(Mailer, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        # after an email is sent successfully, 
        # the user is redirected to the success page
        return reverse("mail_success")

    def form_valid(self, form):

        kindOptions = {"Humans": "H", "ZOMBIES":"Z"}

        sender = "hvzwattest@gmail.com"
        # sender = "mod@claremonthvz.org"

        if form.is_valid():
            # send email using information from the self.cleaned_data dictionary
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            recipient_title = form.cleaned_data['recipient']
            schoolSelection = form.cleaned_data['school']

            # filter players by team
            kind_recipients = []
            kind_label = "[" + recipient_title + "]"
            # Using a dictionary to have more robust way to select players
            if (recipient_title in kindOptions):
                kind_recipients = [p.user.email for p in Player.current_players() if p.team == kindOptions[recipient_title]]
            else:
                # Default recipients list is all players
                kind_recipients = [p.user.email for p in Player.current_players()]
           
            # add team tag to subject line
            subject = kind_label + subject
           
           # filter players by school, add school tag to subject line
            school_recipients = []
            for schools in schoolSelection:
                school_label = "[" + schools + "]"
                subject = school_label + subject
                school_recipients.append([p.user.email for p in Player.current_players() if p.school.name == schools])
            
            # flatten the list of lists
            school_recipients = [item for sublist in school_recipients for item in sublist]
            
            # combine two lists to get to right list of recipients
            recipients = []
            if(len(school_recipients) == 0):
                recipients = kind_recipients
            else:
                recipients = list(set(kind_recipients).intersection(set(school_recipients)))

            # Create an EmailMessage objwct with our given parameters
            mailBag = EmailMessage(subject, body, sender, [], recipients)
            # Check if the user uploaded an attachment (POST), and attach 
            # it to all messages if so

            if self.request.method == 'POST':
                if(self.request.FILES):
                    attachment = self.request.FILES['attachment']
                    mailBag.attach(attachment.name, attachment.read(), attachment.content_type)

            # Send the email in batches of 100. Each batch is sent from a different email in 
            # the list of sender accounts above (EMAIL_LIST)
            recipLen = len(recipients)
            x = 0
            while recipLen > 0:
                if(recipLen > 100):
                    batch = recipients[(x*100):(x*100)+99]
                    mailBag.bcc = batch
                    mailBag.connection = EmailBackend(username = EMAIL_LIST[x], password = EMAIL_PW_LIST[x])
                else:
                    batch = recipients[(x*100):(x*100)+recipLen]
                    mailBag.bcc = batch
                    mailBag.connection = EmailBackend(username = EMAIL_LIST[x], password = EMAIL_PW_LIST[x])
                # Send the emails out!
                mailBag.send(fail_silently=False)
                x += 1
                recipLen -= 100
        
        return super(Mailer, self).form_valid(form)
