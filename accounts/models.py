from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save



def generateAlcherId(fullname):
	latUserID = User.objects.latest('id').id
	newUserID=latUserID+1
	fullname_trim = fullname.replace(" ","")
	fullname_trim = fullname_trim.replace("'","")
	fullname_trim = fullname_trim[:3].upper()
	alcher_id= "ALC-"+fullname_trim+"-"+str(newUserID)
	return alcher_id



class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
        alcher_id = models.CharField(max_length=20, unique=True)
        fullname = models.CharField(max_length=200)
        phone = models.CharField(max_length=13,blank=True,null=True)
        alternate_phone = models.CharField(max_length=13,blank=True,null=True)
        college = models.CharField(max_length=100)
        profile_image = models.ImageField(upload_to ='profile/' ,default="profile/profile.png")
        team = models.ForeignKey("accounts.Team",related_name="members",on_delete=models.CASCADE,null=True)
        GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ]
        gender = models.CharField(
                choices = GENDER_CHOICES,
                max_length=1,
                default='M'
                )
        
        def __str__(self):
                return self.alcher_id
        
        def save(self,*args,**kwargs):
            if not self.id :
                alcher_id = generateAlcherId(self.fullname)
                self.alcher_id = alcher_id 
            return super(Profile,self).save(*args,**kwargs)


            

class Team(models.Model) :
    leader = models.OneToOneField(User,related_name="team",on_delete=models.CASCADE)
    team_name = models.CharField(max_length=255,blank=False,null=False)
    team_id = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=255,blank=True)
    state = models.CharField(max_length=255,blank=True)
    

def generateTeamId(name):
	latTeamID = Team.objects.latest('id').id
	newTeamID=latUserID+1
	name_trim = name.replace(" ","")
	name_trim = name_trim.replace("'","")
	name_trim = name_trim[:3].upper()
	team_id= "ALC-TEAM-"+name_trim+"-"+str(newTeamID)
	return team_id

@receiver(pre_save,sender=Team)
def generate_team_id(sender,instance,*args,**kwargs) :
    if not instance.id :
        team_id = generateTeamId(instance.team_name)
        instance.team_id = team_id

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,*args,**kwargs) :
    if created :
        profile ,profile_created= Profile.objects.get_or_create(user=instance)