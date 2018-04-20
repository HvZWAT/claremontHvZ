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



EMAIL_LIST = ["hvzwattest@gmail.com", "hvzwattest1@gmail.com", "hvzwattest2@gmail.com", "hvzwattest3@gmail.com", "hvzwattest4@gmail.com"]
EMAIL_PW_LIST = ["claremonthvz", "claremonthvz1", "claremonthvz2", "claremonthvz", "claremonthvz4"]

emailList = emailList = [
 'test0@example.com',
 'test1@example.com',
 'test2@example.com',
 'test3@example.com',
 'test4@example.com',
 'test5@example.com',
 'test6@example.com',
 'test7@example.com',
 'test8@example.com',
 'test9@example.com',
 'test10@example.com',
 'test11@example.com',
 'test12@example.com',
 'test13@example.com',
 'test14@example.com',
 'test15@example.com',
 'test16@example.com',
 'test17@example.com',
 'test18@example.com',
 'test19@example.com',
 'aschulze@hmc.edu',
 'test21@example.com',
 'test22@example.com',
 'test23@example.com',
 'test24@example.com',
 'test25@example.com',
 'test26@example.com',
 'test27@example.com',
 'test28@example.com',
 'test29@example.com',
 'test30@example.com',
 'test31@example.com',
 'test32@example.com',
 'test33@example.com',
 'test34@example.com',
 'test35@example.com',
 'test36@example.com',
 'test37@example.com',
 'test38@example.com',
 'test39@example.com',
 'test40@example.com',
 'test41@example.com',
 'test42@example.com',
 'test43@example.com',
 'test44@example.com',
 'test45@example.com',
 'test46@example.com',
 'test47@example.com',
 'test48@example.com',
 'test49@example.com',
 'test50@example.com',
 'test51@example.com',
 'test52@example.com',
 'test53@example.com',
 'test54@example.com',
 'test55@example.com',
 'test56@example.com',
 'test57@example.com',
 'test58@example.com',
 'test59@example.com',
 'test60@example.com',
 'test61@example.com',
 'test62@example.com',
 'test63@example.com',
 'test64@example.com',
 'test65@example.com',
 'test66@example.com',
 'test67@example.com',
 'test68@example.com',
 'test69@example.com',
 'test70@example.com',
 'test71@example.com',
 'test72@example.com',
 'test73@example.com',
 'test74@example.com',
 'test75@example.com',
 'test76@example.com',
 'test77@example.com',
 'test78@example.com',
 'test79@example.com',
 'test80@example.com',
 'test81@example.com',
 'test82@example.com',
 'test83@example.com',
 'test84@example.com',
 'test85@example.com',
 'test86@example.com',
 'test87@example.com',
 'test88@example.com',
 'test89@example.com',
 'test90@example.com',
 'test91@example.com',
 'test92@example.com',
 'test93@example.com',
 'test94@example.com',
 'test95@example.com',
 'test96@example.com',
 'test97@example.com',
 'test98@example.com',
 'test99@example.com',
 'test100@example.com',
 'ctan@hmc.edu',
 'test102@example.com',
 'test103@example.com',
 'test104@example.com',
 'test105@example.com',
 'test106@example.com',
 'test107@example.com',
 'test108@example.com',
 'test109@example.com',
 'test110@example.com',
 'test111@example.com',
 'test112@example.com',
 'test113@example.com',
 'test114@example.com',
 'test115@example.com',
 'test116@example.com',
 'test117@example.com',
 'test118@example.com',
 'test119@example.com',
 'test120@example.com',
 'test121@example.com',
 'test122@example.com',
 'test123@example.com',
 'test124@example.com',
 'test125@example.com',
 'test126@example.com',
 'test127@example.com',
 'test128@example.com',
 'test129@example.com',
 'test130@example.com',
 'test131@example.com',
 'test132@example.com',
 'test133@example.com',
 'test134@example.com',
 'test135@example.com',
 'test136@example.com',
 'test137@example.com',
 'test138@example.com',
 'test139@example.com',
 'test140@example.com',
 'test141@example.com',
 'test142@example.com',
 'test143@example.com',
 'test144@example.com',
 'test145@example.com',
 'test146@example.com',
 'test147@example.com',
 'test148@example.com',
 'test149@example.com',
 'test150@example.com',
 'test151@example.com',
 'test152@example.com',
 'test153@example.com',
 'test154@example.com',
 'test155@example.com',
 'test156@example.com',
 'test157@example.com',
 'test158@example.com',
 'test159@example.com',
 'test160@example.com',
 'test161@example.com',
 'test162@example.com',
 'test163@example.com',
 'test164@example.com',
 'test165@example.com',
 'test166@example.com',
 'test167@example.com',
 'test168@example.com',
 'test169@example.com',
 'test170@example.com',
 'test171@example.com',
 'test172@example.com',
 'test173@example.com',
 'test174@example.com',
 'test175@example.com',
 'test176@example.com',
 'test177@example.com',
 'test178@example.com',
 'test179@example.com',
 'test180@example.com',
 'test181@example.com',
 'test182@example.com',
 'test183@example.com',
 'test184@example.com',
 'test185@example.com',
 'test186@example.com',
 'test187@example.com',
 'test188@example.com',
 'test189@example.com',
 'test190@example.com',
 'test191@example.com',
 'test192@example.com',
 'test193@example.com',
 'test194@example.com',
 'test195@example.com',
 'test196@example.com',
 'test197@example.com',
 'test198@example.com',
 'test199@example.com',
 'test200@example.com',
 'test201@example.com',
 'test202@example.com',
 'test203@example.com',
 'test204@example.com',
 'test205@example.com',
 'test206@example.com',
 'test207@example.com',
 'test208@example.com',
 'test209@example.com',
 'test210@example.com',
 'test211@example.com',
 'test212@example.com',
 'test213@example.com',
 'test214@example.com',
 'test215@example.com',
 'test216@example.com',
 'test217@example.com',
 'test218@example.com',
 'test219@example.com',
 'test220@example.com',
 'test221@example.com',
 'test222@example.com',
 'test223@example.com',
 'test224@example.com',
 'test225@example.com',
 'test226@example.com',
 'test227@example.com',
 'test228@example.com',
 'test229@example.com',
 'test230@example.com',
 'test231@example.com',
 'test232@example.com',
 'test233@example.com',
 'test234@example.com',
 'test235@example.com',
 'test236@example.com',
 'test237@example.com',
 'test238@example.com',
 'test239@example.com',
 'test240@example.com',
 'test241@example.com',
 'test242@example.com',
 'test243@example.com',
 'test244@example.com',
 'test245@example.com',
 'test246@example.com',
 'test247@example.com',
 'test248@example.com',
 'test249@example.com',
 'test250@example.com',
 'test251@example.com',
 'test252@example.com',
 'test253@example.com',
 'test254@example.com',
 'test255@example.com',
 'test256@example.com',
 'test257@example.com',
 'test258@example.com',
 'test259@example.com',
 'test260@example.com',
 'test261@example.com',
 'test262@example.com',
 'test263@example.com',
 'test264@example.com',
 'test265@example.com',
 'test266@example.com',
 'test267@example.com',
 'test268@example.com',
 'test269@example.com',
 'test270@example.com',
 'test271@example.com',
 'test272@example.com',
 'test273@example.com',
 'test274@example.com',
 'test275@example.com',
 'test276@example.com',
 'test277@example.com',
 'test278@example.com',
 'test279@example.com',
 'test280@example.com',
 'test281@example.com',
 'test282@example.com',
 'test283@example.com',
 'test284@example.com',
 'test285@example.com',
 'test286@example.com',
 'test287@example.com',
 'test288@example.com',
 'test289@example.com',
 'test290@example.com',
 'test291@example.com',
 'test292@example.com',
 'test293@example.com',
 'test294@example.com',
 'test295@example.com',
 'test296@example.com',
 'test297@example.com',
 'test298@example.com',
 'test299@example.com',
 'test300@example.com',
 'test301@example.com',
 'test302@example.com',
 'test303@example.com',
 'test304@example.com',
 'test305@example.com',
 'test306@example.com',
 'test307@example.com',
 'test308@example.com',
 'test309@example.com',
 'test310@example.com',
 'test311@example.com',
 'test312@example.com',
 'test313@example.com',
 'test314@example.com',
 'test315@example.com',
 'test316@example.com',
 'test317@example.com',
 'test318@example.com',
 'test319@example.com',
 'test320@example.com',
 'test321@example.com',
 'test322@example.com',
 'test323@example.com',
 'test324@example.com',
 'test325@example.com',
 'test326@example.com',
 'test327@example.com',
 'test328@example.com',
 'test329@example.com',
 'test330@example.com',
 'test331@example.com',
 'test332@example.com',
 'test333@example.com',
 'test334@example.com',
 'test335@example.com',
 'test336@example.com',
 'test337@example.com',
 'test338@example.com',
 'test339@example.com',
 'test340@example.com',
 'test341@example.com',
 'test342@example.com',
 'test343@example.com',
 'test344@example.com',
 'test345@example.com',
 'test346@example.com',
 'test347@example.com',
 'test348@example.com',
 'test349@example.com',
 'test350@example.com',
 'test351@example.com',
 'test352@example.com',
 'test353@example.com',
 'test354@example.com',
 'test355@example.com',
 'test356@example.com',
 'test357@example.com',
 'test358@example.com',
 'test359@example.com',
 'test360@example.com',
 'test361@example.com',
 'test362@example.com',
 'test363@example.com',
 'test364@example.com',
 'test365@example.com',
 'test366@example.com',
 'test367@example.com',
 'test368@example.com',
 'test369@example.com',
 'test370@example.com',
 'test371@example.com',
 'test372@example.com',
 'test373@example.com',
 'test374@example.com',
 'test375@example.com',
 'test376@example.com',
 'test377@example.com',
 'test378@example.com',
 'test379@example.com',
 'test380@example.com',
 'test381@example.com',
 'test382@example.com',
 'test383@example.com',
 'test384@example.com',
 'test385@example.com',
 'test386@example.com',
 'test387@example.com',
 'test388@example.com',
 'test389@example.com',
 'test390@example.com',
 'test391@example.com',
 'test392@example.com',
 'test393@example.com',
 'test394@example.com',
 'test395@example.com',
 'test396@example.com',
 'test397@example.com',
 'test398@example.com',
 'test399@example.com',
 'cvalleroy@hmc.edu',
 'test401@example.com',
 'test402@example.com',
 'test403@example.com',
 'test404@example.com',
 'test405@example.com',
 'test406@example.com',
 'test407@example.com',
 'test408@example.com',
 'test409@example.com',
 'test410@example.com',
 'test411@example.com',
 'test412@example.com',
 'test413@example.com',
 'test414@example.com',
 'test415@example.com',
 'test416@example.com',
 'test417@example.com',
 'test418@example.com',
 'test419@example.com',
 'test420@example.com',
 'test421@example.com',
 'test422@example.com',
 'test423@example.com',
 'test424@example.com',
 'test425@example.com',
 'test426@example.com',
 'test427@example.com',
 'test428@example.com',
 'test429@example.com',
 'test430@example.com',
 'test431@example.com',
 'test432@example.com',
 'test433@example.com',
 'test434@example.com',
 'test435@example.com',
 'test436@example.com',
 'test437@example.com',
 'test438@example.com',
 'test439@example.com',
 'test440@example.com',
 'test441@example.com',
 'test442@example.com',
 'test443@example.com',
 'test444@example.com',
 'test445@example.com',
 'test446@example.com',
 'test447@example.com',
 'test448@example.com',
 'test449@example.com',
 'test450@example.com',
 'test451@example.com',
 'test452@example.com',
 'test453@example.com',
 'test454@example.com',
 'test455@example.com',
 'test456@example.com',
 'test457@example.com',
 'test458@example.com',
 'test459@example.com',
 'test460@example.com',
 'test461@example.com',
 'test462@example.com',
 'test463@example.com',
 'test464@example.com',
 'test465@example.com',
 'test466@example.com',
 'test467@example.com',
 'test468@example.com',
 'test469@example.com',
 'test470@example.com',
 'test471@example.com',
 'test472@example.com',
 'test473@example.com',
 'test474@example.com',
 'test475@example.com',
 'test476@example.com',
 'test477@example.com',
 'test478@example.com',
 'test479@example.com',
 'test480@example.com',
 'test481@example.com',
 'test482@example.com',
 'test483@example.com',
 'test484@example.com',
 'test485@example.com',
 'test486@example.com',
 'test487@example.com',
 'test488@example.com',
 'test489@example.com',
 'test490@example.com',
 'test491@example.com',
 'test492@example.com',
 'test493@example.com',
 'test494@example.com',
 'test495@example.com',
 'test496@example.com',
 'test497@example.com',
 'test498@example.com',
 'jkunzelman@hmc.edu',
 'test500@example.com',
 'collinvalleroy@hotmail.com']

def json_get_all_emails(request):
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
        # after the mail is sent successfully, it goes to the success page
        return reverse("mail_success")

    def form_valid(self, form):

        kindOptions = {"Humans": "H", "ZOMBIES":"Z"}

        sender = "hvzwattest@gmail.com"

        # sender = "mod@claremonthvz.org"
        if form.is_valid():
            # send email using the self.cleand_data dictionary
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            recipient_title = form.cleaned_data['recipient']


            schoolSelection = form.cleaned_data['school']

            kind_recipients = []
            kind_label = "[" + recipient_title + "]"
            # Using a dictionary to have more robust way to select players
            if (recipient_title in kindOptions):
                kind_recipients = [p.user.email for p in Player.current_players() if p.team == kindOptions[recipient_title]]
            else:
                # Default recipients list is all players
                kind_recipients = [p.user.email for p in Player.current_players()]
           
            subject = kind_label + subject
           
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
            # it to all messages in the mailBag

            attachment = 0
            if self.request.method == 'POST':
                if(self.request.FILES):
                    attachment = self.request.FILES['attachment']
                    mailBag.attach(attachment.name, attachment.read(), attachment.content_type)

            # recipients = emailList
            recipLen = len(emailList)
            x = 0
            y = 0
            while recipLen > 0:
                if(recipLen > 100):
                    batch = emailList[(y*100):(y*100)+100]
                    mailBag.bcc = batch
                    mailBag.connection = EmailBackend(username = EMAIL_LIST[x], password = EMAIL_PW_LIST[x])
                
                else:
                    batch = emailList[(y*100):(y*100)+recipLen]
                    mailBag.bcc = batch
                    mailBag.connection = EmailBackend(username = EMAIL_LIST[x], password = EMAIL_PW_LIST[x])
                
                # Send the emails out!
                mailBag.send(fail_silently=False)
                y += 1
                x += 1
                if x > 4:
                    x = 0
                recipLen -= 100
        
        return super(Mailer, self).form_valid(form)
