from django.test import TestCase, Client
from django.contrib.auth.models import User
from hvz.api.forms import MailerForm
from hvz.api.views import Mailer
from hvz.main import models
import random
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
# Create your tests here.

# Try random combinations of filters
class MailerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = 'password'
        self.my_admin = User.objects.create_superuser('test', 'test@test.edu', self.password)
        call_command('newgame')
        call_command('randomplayers')
        call_command('randomhistory')
        self.game = models.Game.nearest_game()

    def test_page_access(self):
        # should be unable to access the mailer page without logging in
        response = self.client.get('/api/mailer')
        self.assertEqual(response.status_code, 302)

        # verify login
        login = self.client.login(username=self.my_admin.username, password=self.password)
        self.assertEqual(login, True)

        # now access mailer
        response = self.client.get('/api/mailer', follow=True)
        self.assertEqual(response.status_code, 200)
        
        self.client.logout()

    def test_form(self):
        login = self.client.login(username=self.my_admin.username, password=self.password)
        response = self.client.get('/api/mailer', follow=True)
        num_Players = len(models.Player.current_players())

        KindCHOICES = [
            "All",
            "Humans",
            "Zombies"]

        SchoolCHOICES = [
            'Mudd',
            'CMC',
            'Pitzer',
            'Pomona',
            'Scripps']

        kind = random.choice(KindCHOICES)
        numschools = random.choice(range(len(SchoolCHOICES)))
        schools = random.sample(SchoolCHOICES, numschools)

        recipients = [p.user.email for p in models.Player.current_players() if p.team == kind and p.school in schools]

        form = MailerForm(data={'recipient' : kind,
            'school' : schools,
            'subject' : "test",
            'body': "This is a test"
            })

        mailObj = Mailer()

        self.assertEqual(form.data['recipient'], kind)
        self.assertEqual(form.data['school'], schools)
        self.assertEqual(form.data['subject'], "test")
        self.assertEqual(form.data['body'], "This is a test")
        self.assertTrue(form.is_valid())
        mailObj.form_valid(form)
        self.assertEqual(len(django.mail.outbox), len(recipients))


        



