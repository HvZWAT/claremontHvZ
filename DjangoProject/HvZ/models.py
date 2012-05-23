from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from datetime import datetime,timedelta

from constants import *

##################
# Building Stuff #
##################
class School(models.Model):
    """The 7Cs"""
    name = models.CharField(max_length=7, help_text="The name of the college")
    def __unicode__(self):
        """Return a string representation of the School"""
        return self.name

class Building(models.Model):
    """Building are locations on the 7Cs. Most important are dorms and
    landmarks where missions are"""
    
    name = models.CharField(max_length=100, help_text="The name of the building")
    nick = models.CharField(max_length=100, blank=True, help_text="A nickname of the building")
    campus = models.ForeignKey(School,blank=True,null=True, help_text="The school is the building a part of")
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, help_text="The latitude of the building")
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, help_text="The longitude of the building")
    
    def __unicode__(self):
        """Return a string representation of the building"""
        return "%s (%s)" % (self.name, self.campus)

    def get_kinds(self):
        """Return a list of all building types that the building is"""
        r = []
        for k in BuildingKind.objects.filter(building=self):
            r.append(k.get_kind())
        return r

class BuildingKind(models.Model):
    """BuildingKinds are the way to account for buildings having multiple varieties"""
    building = models.ForeignKey(Building, help_text="The building receiving a kind")
    kind = models.CharField(max_length=1,choices=BUILDING_LEGEND, help_text="The kind of building it is")

    def __unicode__(self):
        """Return a string representation of the building's kind."""
        return "%s as a %s"%(self.building.name, self.get_kind())


class Dorm(Building):
    """Dorms are buildings that people live in."""
    residents = models.PositiveSmallIntegerField(default=0)

class Academic(Building):
    """Academics are academic buildings where classes are held."""
    #students_day_time is how many students are in class there at a given time.
    #It is so we don't have to manually calculate it based on every arrive and leave.
    #For purposes of calculating it, assume that they are present during the arrive block, leave block, and each block between.
    students_T_E = models.PositiveSmallIntegerField(default=0, help_text="Students in class Tuesday in the early morning")
    students_T_M = models.PositiveSmallIntegerField(default=0, help_text="Students in class Tuesday in the morning")
    students_T_L = models.PositiveSmallIntegerField(default=0, help_text="Students in class Tuesday during lunch")
    students_T_A = models.PositiveSmallIntegerField(default=0, help_text="Students in class Tuesday in the afternoon")
    students_T_B = models.PositiveSmallIntegerField(default=0, help_text="Students in class Tuesday before dinner")
    students_T_D = models.PositiveSmallIntegerField(default=0, help_text="Students in class Tuesday during dinner")
    students_T_I = models.PositiveSmallIntegerField(default=0, help_text="Students in class Tuesday during the night mission")
    students_T_N = models.PositiveSmallIntegerField(default=0, help_text="Students in class Tuesday late at night")

    students_W_E = models.PositiveSmallIntegerField(default=0, help_text="Students in class Wednesday in the early morning")
    students_W_M = models.PositiveSmallIntegerField(default=0, help_text="Students in class Wednesday in the morning")
    students_W_L = models.PositiveSmallIntegerField(default=0, help_text="Students in class Wednesday during lunch")
    students_W_A = models.PositiveSmallIntegerField(default=0, help_text="Students in class Wednesday in the afternoon")
    students_W_B = models.PositiveSmallIntegerField(default=0, help_text="Students in class Wednesday before dinner")
    students_W_D = models.PositiveSmallIntegerField(default=0, help_text="Students in class Wednesday during dinner")
    students_W_I = models.PositiveSmallIntegerField(default=0, help_text="Students in class Wednesday during the night mission")
    students_W_N = models.PositiveSmallIntegerField(default=0, help_text="Students in class Wednesday late at night")

    students_R_E = models.PositiveSmallIntegerField(default=0, help_text="Students in class Thursday in the early morning")
    students_R_M = models.PositiveSmallIntegerField(default=0, help_text="Students in class Thursday in the morning")
    students_R_L = models.PositiveSmallIntegerField(default=0, help_text="Students in class Thursday during lunch")
    students_R_A = models.PositiveSmallIntegerField(default=0, help_text="Students in class Thursday in the afternoon")
    students_R_B = models.PositiveSmallIntegerField(default=0, help_text="Students in class Thursday before dinner")
    students_R_D = models.PositiveSmallIntegerField(default=0, help_text="Students in class Thursday during dinner")
    students_R_I = models.PositiveSmallIntegerField(default=0, help_text="Students in class Thursday during the night mission")
    students_R_N = models.PositiveSmallIntegerField(default=0, help_text="Students in class Thursday late at night")

    students_F_E = models.PositiveSmallIntegerField(default=0, help_text="Students in class Friday in the early morning")
    students_F_M = models.PositiveSmallIntegerField(default=0, help_text="Students in class Friday in the morning")
    students_F_L = models.PositiveSmallIntegerField(default=0, help_text="Students in class Friday during lunch")
    students_F_A = models.PositiveSmallIntegerField(default=0, help_text="Students in class Friday in the afternoon")
    students_F_B = models.PositiveSmallIntegerField(default=0, help_text="Students in class Friday before dinner")
    students_F_D = models.PositiveSmallIntegerField(default=0, help_text="Students in class Friday during dinner")
    students_F_I = models.PositiveSmallIntegerField(default=0, help_text="Students in class Friday during the night mission")
    students_F_N = models.PositiveSmallIntegerField(default=0, help_text="Students in class Friday late at night")

###############
# Game Things #
###############
class Game(models.Model):
    """Games are the events that tie everything together"""
    start_date = models.DateField(help_text="The date of the first Tuesday of the game")

    def __unicode__(self):
        """Return a string representation of the game"""
        if self.start_date.month<6:
            return "Spring %s"%(str(self.start_date.year)[-2:])
        else:
            return "Fall %s"%(str(self.start_date.year)[-2:])


class Rule(models.Model):
    """Rules are each individual rule in the game"""
    CATS = (
            ("L","Location"),
            ("C","Class"),
            ("B","Basic")
    )
    title = models.CharField(max_length=30, help_text="The name of the rule")
    description = models.TextField(blank=False, help_text="A summary or explanation of the rule")
    category= models.CharField(max_length=1,choices=CATS, help_text="Which basic kind of rule is it?")
    examples = models.TextField(blank=True, help_text="Specific details, examples, clarifications, or exceptions related to the rule that won't come up often.")
    youtube = models.URLField(verify_exists=True, blank=True, help_text="A link to a youtube video of the rule.")
    image = models.ImageField(upload_to="img/rule/", blank=True, help_text="A picture, diagram, graph, or photo of the rule.")
    location = models.ForeignKey(Building, blank=True, null=True, help_text="If the rule is about a single location, include it here.")
    priority = models.PositiveSmallIntegerField(default=0, help_text="Rules with a higher priority appear earlier in the list.")

    def __unicode__(self):
        """Return a string representation of the rule"""
        return str(self.title)

#################
# Mission Stuff #
#################
class Mission(models.Model):
    """Missions are events that occur during the game."""

    #Basic info
    human_title = models.CharField(max_length=30, blank=True)
    zombie_title = models.CharField(max_length=30, blank=True)
    game = models.ForeignKey(Game)
    day = models.CharField(max_length=1, choices=DAYS)
    kind = models.CharField(max_length=1, choices=MISSION_LEGEND)
    show_players = models.CharField(max_length=1, choices=VISIBILITY, default="M")
    result = models.CharField(max_length=2, choices=VICTORY, default="N")

    # This is story stuff. Both sides see the quote
    # story is what they see before and during the mission
    # outcome is what they see after the mission
    quote = models.TextField(blank=True)
    human_story = models.TextField(blank=True)
    human_outcome = models.TextField(blank=True)
    zombie_story = models.TextField(blank=True)
    zombie_outcome = models.TextField(blank=True)

    # This is what the teams see in the "rules" or "mechanics" section
    # for each mission, it also includes goals
    human_rules = models.TextField(blank=True)
    zombie_rules = models.TextField(blank=True)

    # This is what the teams see in the "rewards" section for each
    # mission
    human_reward = models.TextField(blank=True)
    zombie_reward = models.TextField(blank=True)

    # This is what response is returned if someone texts "mission",
    # "mission NPC", or "mission Legendary" to us
    human_SMS = models.CharField(max_length=140,blank=True)
    zombie_SMS = models.CharField(max_length=140,blank=True)

    def get_result_order(self):
        """Returns the order of the outcome of the mission so it can be sorted (0, 1, 2, 3, 4, 5)"""
        return VICTORY_ORDER[self.result]

    def get_title(self,team):
        """Returns the title of the mission based on which team is seeing it"""
        if self.show_players=="B" or self.show_players==team:
            if team=="H":
		return self.human_title
            else:
		return self.zombie_title
	else:
            return "No title is visible for this mission yet."

    def get_story(self,team):
        """Returns the story of the mission based on the team and whether it is over"""
	if self.show_players=="B" or self.show_players==team:
		ret = ""
		if team=="H":
			ret+=self.human_story
		else:
			ret+=self.zombie_story

		if self.result!="N":
			if team=="H":
				ret+="<br/>"+self.human_outcome
			else:
				ret+="<br/>"+self.zombie_outcome
	else:
		ret =  "No Story is visible for this mission yet."
	return ret

    def get_reward(self,team):
        """Returns the reward for the mission based on the team"""
	if self.show_players=="B" or self.show_players==team:
		if team=="H":
			return self.human_reward
		else:
			return self.zombie_reward
	else:
		return "No Reward is visible for this mission yet."

    def get_SMS(self,team):
        """Returns the SMS based on the team."""
        if self.show_players=="B" or self.show_players==team:
		if team=="H":
			return self.human_SMS
		else:
			return self.zombie_SMS
	else:
		return "No SMS is available for this mission yet."

    def __unicode__(self):
        """Returns a string representation of the game"""
        return "%s: %s/%s" % (self.game,
                              self.human_title,
                              self.zombie_title)

class MissionPic(models.Model):
    """MissionPics are how you store pictures for missions"""
    mission = models.ForeignKey(Mission)
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to="img/mission/")
    visibility = models.CharField(max_length=1, choices=VISIBILITY)

    def __unicode__(self):
        """Returns a string representation of the mission pic"""
        return "%s for %s"%(self.title, str(self.mission))

class MissionPoint(models.Model):
    """MissionPoints are how you indicate points that are important to missions"""
    mission = models.ForeignKey(Mission)
    location = models.ForeignKey(Building)
    kind = models.CharField(max_length=1, choices=LOCATION_LEGEND)
    visibility = models.CharField(max_length=1, choices=VISIBILITY)

    def __unicode__(self):
        """Returns a string represntation of the mission point."""
        return "%s %s for %s"%(self.get_kind(), str(self.location), str(self.mission))

class Plot(models.Model):
    """Plots are story elements that are not part of missions"""
    title = models.CharField(max_length=30)
    game = models.ForeignKey(Game)
    show_players = models.CharField(max_length=1,choices=VISIBILITY)
    story = models.TextField()
    reveal_time = models.DateTimeField()

    def get_tile(self,team):
        """Returns the title that should be visible for the given team"""
        if self.reveal_time<datetime.now() and (self.show_players=="B" or self.show_players==team):
		return self.title
	else:
		return "This plot point has not been revealed yet."
    def get_story(self,team):
        """Returns the story that should be visible for the given team"""
        if self.reveal_time<datetime.now() and (self.show_players=="B" or self.show_players==team):
		return self.story
	else:
		return "This plot point has not been revealed yet."
    
    def __unicode__(self):
        """Returns a string representation of the plot point"""
	return "%s: %s" % (self.game,self.title)
    
################
# Player Stuff #
################
class Player(models.Model):
    """extra information about users that doesn't involve messing with the django users model"""
    user = models.OneToOneField(User)
    school = models.ForeignKey(School, blank=True, null=True)
    dorm = models.ForeignKey(Dorm, blank=True, null=True)
    class_year = models.CharField(max_length=1, choices=CLASS_YEAR, blank=True)
    cell = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    bad_meals = models.PositiveSmallIntegerField(default=0)
    bad_posts = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        """Returns a string representation of the user"""
        return "%s %s" % (self.user.first_name, self.user.last_name)

class PlayerCellSetting(models.Model):
    """Player Cell Phone settings"""
    player = models.OneToOneField(Player)
    
    emergency = models.BooleanField(default=True)
    send = models.BooleanField(default=False)
    mission_announce = models.BooleanField(default=False)
    mission_update = models.BooleanField(default=False)
    npc_announce = models.BooleanField(default=False)
    npc_update = models.BooleanField(default=False)
    legendary_announce = models.BooleanField(default=False)
    legendary_update = models.BooleanField(default=False)

    def __unicode__(self):
        """Returns a string representation of the player's settings"""
        return "%s's Settings" % self.player

    def quit_cell(self):
        """Command to unsubscribe from all texting services"""
        self.emergency = False
        self.send = False
        self.mission_announce = False
        self.mission_update = False
        self.npc_announce = False
        self.npc_update = False
        self.legendary_announce = False
        self.legendary_update = False

class PlayerProfileSetting(models.Model):
    """Player profile information"""
    player = models.OneToOneField(Player)
    human_pic = models.ImageField(upload_to="img/profile/", blank=True)
    zombie_pic = models.ImageField(upload_to="img/profile/", blank=True)
    bio = models.TextField(blank=True)

    #visibility related settings
    show_school = models.CharField(max_length=1, choices=VISIBILITY, default="B")
    show_dorm = models.CharField(max_length=1, choices=VISIBILITY, default="B")
    show_year = models.CharField(max_length=1, choices=VISIBILITY, default="B")
    show_cell = models.CharField(max_length=1, choices=VISIBILITY, default="B")

    def __unicode__(self):
        """Returns a string representation of the player's profile"""
        return "%s's Profile" % self.player

class PlayerWebSetting(models.Model):
    """Settings for how the user expereiences the Website"""
    player = models.OneToOneField(Player)

###################
# Character Stuff #
###################
class Character(models.Model):
    """Characters are the instances of players in games"""
    TEAMS = (
             ("H","Humans"),
             ("Z","Zombies")
    )
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    team = models.CharField(max_length=1, choices=TEAMS, default="H")
    upgrade = models.CharField(max_length=30,blank=True)
    hardcore = models.BooleanField(default=False)

    #Meals is now total meals to avoid a costly DB lookup when you want to know how many meals someone has
    meals = models.PositiveSmallIntegerField(default=0, blank=False)

    #These 3 fields are redundant most of the time, but are useful for archiving games
    lives_in = models.ForeignKey(Dorm, blank=True, null=True)
    goes_to = models.ForeignKey(School, blank=True, null=True)
    year = models.CharField(max_length=1, choices=CLASS_YEAR, blank=True, null=True)
    
    def __unicode__(self):
        """Returns a string representation of the character"""
        return "%s (%s)" %(str(self.player),str(self.game))

    def can_eat(self):
        """Returns true if the user has few enough bad meal attempts that they are allowed to try eating"""
        if self.player.bad_meals<10:
            return True
        else:
            return False

    def can_post(self):
        """Returns true if the user has few enough bad post attempts that they are allowed to post on the forums"""
        if self.player.bad_posts<10:
            return True
        else:
            return False

    def increment_bad_meals(self):
        """Increases the number of bad meal attempts that a character has made"""
        p = self.player
        p.bad_meals += 1

    def increment_bad_posts(self):
        """Increases the number of bad post attempts that a character has made"""
        p = self.player
        p.bad_posts += 1

class FeedCode(models.Model):
    """FeedCodes are the way that meals are handled. Now that there are so many new options, it has been pulled out."""
    #This should have a mechanism to check that a feed code is unique for the past 10 games
    #This should also have a mechanism to make sure that only the legitimate letters are used

    #If blank, then the meal is just a reward not linked to a player
    character = models.ForeignKey(Character, blank=True, null=True)

    #Game is required because some meals aren't linked to characters but should still only be usable for a specific game.
    game = models.ForeignKey(Game)

    #code is the 6 letter feed code
    #This only legitimately contain the letters A, C, D, E, K, L, N, P, S, T, W, and Z.
    code = models.CharField(max_length=6)

    #value is how many meals the eater's mealcount should be incremented by when they eat this card
    value = models.PositiveSmallIntegerField(default=1)

    #turns is true if eating this code turns the player, if false they stay human after having this card eaten
    #the meals page and timeline page should note this as "almost ate", "barely escaped", or the like
    turns = models.BooleanField(default=True)

    def __unicode__(self):
        """Returns a string representation of the meal"""
        return "%s's code: %s"%(self.get_character(),self.code)        

class Meal(models.Model):
    """Meals are what happens when one player eats another"""
    #A bunch of validation should be added to this...
    eater = models.ForeignKey(Character, related_name="eater")
    eaten = models.ForeignKey(Character, related_name="eaten", blank=True, null=True)
    feed = models.ForeignKey(FeedCode)
    game = models.ForeignKey(Game)
    time = models.DateTimeField()
    location = models.ForeignKey(Building, blank=True, null=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        """Returns a string representation of a meal"""
        if self.feed.turns:
            return "%s ate %s (%s)"%(str(self.eater),str(self.eaten),str(self.feed.code))
        else:
            return "%s (%s) escaped from %s"%(str(self.eaten),str(self.feed.code),str(self.eater))

class Classes(models.Model):
    """Classes are character enrollment in courses during a game. It exists so they can coordinate arriving and leaving in groups."""
    character = models.ForeignKey(Character)
    classroom = models.ForeignKey(Academic)
    day = models.CharField(max_length=1, choices=DAYS)
    arrive = models.CharField(max_length=1, choices=TIMES)
    leave = models.CharField(max_length=1, choices=TIMES)

    def __unicode__(self):
        """Returns a string representation of the person in class"""
        return str(self.character)+" is in "+str(self.classroom)+" on "+self.get_day()+" from "+self.get_arrive()+" until "+self.get_leave()

###############
# Squad Stuff #
###############
class Squad(models.Model):
    """Squads are self organized groups of players"""
    name = models.CharField(max_length=255);
    game = models.ForeignKey(Game)
    description = models.TextField()
    icon = models.ImageField(upload_to="icons/squads/", blank=True)

    def __unicode__(self):
        """Returns a string representation of the squad"""
        return str(self.name)

class SquadMember(models.Model):
    """SquadMembers are how people get involved in their squads"""
    #This is set up so that characters can only be part of one squad per game. I think this is ok, unless we make moderator team a squad
    character = models.OneToOneField(Character)
    squad = models.ForeignKey(Squad)
    role = models.CharField(max_length=50)
    moderate = models.BooleanField(default=False)

    def __unicode__(self):
        """Returns a string representation of the character in the squad"""
        return "%s is a %s in %s"%(str(self.character),str(self.role),str(self.squad))
    
###############
# Forum Stuff #
###############
class ForumThread(models.Model):
    """Forum threads are top level posts on a forum."""
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    game = models.ForeignKey(Game)
    create_time = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(Character)
    visibility = models.CharField(max_length=1, choices=VISIBILITY)

    def get_post_count(self):
        """Return the number of posts in the thread"""
	return ForumPost.objects.filter(parent=self).count()

    def get_last_post(self):
        """Return the most recent post in the thread, if it exists"""
	posts = ForumPost.objects.filter(parent=self).order_by('-create_time')
	if posts.exists():
	    return posts[0]
	else:
	    return None

    def __unicode__(self):
        """Return a string representation of the forum thread"""
	return "%s (%s: %s)" % (self.title, self.game, self.get_visibility())

class ForumPost(models.Model):
    """ForumPosts are replies to a ForumThread"""
    parent = models.ForeignKey(ForumThread)
    creator = models.ForeignKey(Character)
    contents = models.TextField(blank=True)
    create_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """Return a string representation of the forum post"""
	return "%s's post to %s at %s" %(str(self.creator),str(self.parent),self.create_time.strftime(TIME_FORMAT))

################
# Achievements #
################
class Award(models.Model):
    """Awards are things that characters can earn over the course of the game. Some are game specific, others are not."""
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=255, blank=True)
    icon = models.ImageField(upload_to="icons/awards/", blank=True)

    def __unicode__(self):
        """Return a string representation of an award"""
        return self.title
        

class Achievement(models.Model):
    """Achievements are instances of characters earning awards"""
    character = models.ForeignKey(Character)
    award = models.ForeignKey(Award)
    earned_time = models.DateTimeField()
    description = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        """Return a string representation of an award"""
        return "%s earned %s"%(str(self.character),str(self.award))

###############################
# Efficiency Stuff for Graphs #
###############################
class MealsPerHour(models.Model):
    """MealsPerHour is the number of meals that have occured in a given hour for a game. It is automatically updated when a meal is entered."""
    game = models.ForeignKey(Game)
    start = models.DateTimeField()
    meals = models.PositiveSmallIntegerField(default=0)

    def recount(self):
        """Counts the number of meals again in case there has been a change"""
        mc = Meal.objects.filter(game=self.game,time__gte=self.start,time__lt=self.start+timedelta(hours=1)).count()
        self.meals = mc

    def __unicode__(self):
        """Return a string representation of the number of meals per hour"""
        dt = self.start
        return "%s in %s has %s meals"%(dt,str(self.game),str(self.meals))

class MealsPerBuilding(models.Model):
    """MealsPerBuilding is the number of meals that have occured at a given location over the course of a game. It is automatically updated when a meal is entered."""
    game = models.ForeignKey(Game)
    location = models.ForeignKey(Building)
    meals = models.PositiveSmallIntegerField(default=0)

    def recount(self):
        """Counts the number of meals again in case there has been a change"""
        mc = Meal.objects.filter(game=self.game,location=self.location).count()
        self.meals = mc

    def __unicode__(self):
        """Returns a string representation of the number of meals a building has accrued in a game"""
        return "%s has %s meals in %s"%(str(self.location), str(self.meals), str(self.game))

########
# Misc #
########
class OnDuty(models.Model):
    """OnDuty is the moderator currently on duty to answer cell phone calls and respond to texts."""
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    mod = models.ForeignKey(Player,limit_choices_to = {'cell__gte':'1', 'user__is_staff':'True'})

    def __unicode__(self):
        """Return a string representation of the moderator on duty"""
        return (
            "%s: %s until %s"%(self.mod.user.first_name, self.start_time.strftime(TIME_FORMAT), self.end_time.strftime(TIME_FORMAT)))

####################
# Signal Functions #
####################

@receiver(post_save, sender=Dorm)
def add_dorm_kind(sender, instance, signal, *args, **kwargs):
    """Add a building kind entry for dorms when someone adds a new dorm"""
    bk = BuildingKind.objects.filter(building=instance,kind="D").exists()
    if not bk:
        k = BuildingKind(building=instance,kind="D")
        k.save()

@receiver(post_save, sender=Academic)
def add_academic_kind(sender, instance, signal, *args, **kwargs):
    """Add a building kind entry for academic buildings when someone adds a new academic building"""
    bk = BuildingKind.objects.filter(building=instance,kind="C").exists()
    if not bk:
        k = BuildingKind(building=instance,kind="C")
        k.save()

@receiver(pre_save, sender=MealsPerHour,dispatch_uid="round hour once")
def round_hour_down(sender, instance, signal, *args, **kwargs):
    instance.start = instance.start-timedelta(minutes=instance.start.minute,seconds=instance.start.second,microseconds=instance.start.microsecond)

@receiver(post_save, sender=Meal)
def add_hour_meal(sender, instance, signal, *args, **kwargs):
    """Add a meal to the MealsPerHour when someone adds a meal"""
    meals = MealsPerHour.objects.filter(game=instance.game,start=instance.time)
    if len(meals)>0:
        m = meals[0]
    else:
        m = MealsPerHour(game=instance.game,start=instance.time-timedelta(minutes=instance.time.minute,seconds=instance.time.second))
    m.recount()
    m.save()

@receiver(post_save, sender=Meal)
def add_building_meal(sender, instance, signal, *args, **kwargs):
    """Add a meal to the MealsPerBuilding when someone adds a meal"""
    meals = MealsPerBuilding.objects.filter(game=instance.game,location=instance.location)
    if len(meals)>0:
        m = meals[0]
    else:
        m = MealsPerBuilding(game=instance.game,location=instance.location)
    m.recount()
    m.save()

@receiver(post_save, sender=Character)
def change_team_visibility(sender, instance, signal, *args, **kwargs):
    """Update the visibility of anything on a player's profile to the team they are currently on when they switch teams"""
    prof = PlayerProfile.objects.filter(player=instance.player)
    if prof:
        if instance.team=="Z":
            if prof.show_school=="H":
                prof.show_school="Z"
            if prof.show_dorm=="H":
                prof.show_dorm="Z"
            if prof.show_year=="H":
                prof.show_year="Z"
            if prof.show_cell=="H":
                prof.show_cell="Z"
        else:
            if prof.show_school=="Z":
                prof.show_school="H"
            if prof.show_dorm=="Z":
                prof.show_dorm="H"
            if prof.show_year=="Z":
                prof.show_year="H"
            if prof.show_cell=="Z":
                prof.show_cell="H"
        prof.save()
