from django.contrib.auth import get_user_model
from django.db import models

User= get_user_model()

#Create your models here
class Project(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	goal = models.IntegerField()
	image = models.URLField()
	is_open = models.BooleanField()
	date_created = models.DateTimeField()
	owner = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='owner_projects'
	)
# but unsure of order for migration plus whether this has to be cross referenced elsewhwere in my code?
	liked_by = models.ManyToManyField(
	User,
	related_name='liked_projects'
	)
class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(
      	'Project',
        on_delete=models.CASCADE,
        related_name='pledges'
	)
    supporter = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='supporter_pledges'
		)
# Ben's assistance with calculating total pledged per project, with option for nothing pledged yet
@property
def total(self):
	pledge_total = self.pledges.aggregate(sum=models.Sum('amount'))['sum']
	if pledge_total == None:
		return 0
	else: 
		return pledge_total

@property
def goal_vs_pledges(self):
        '''    Looks at the goal and compares to the total number of pledges. '''
        goal_balance = self.goal - self.pledge_total
        
        if goal_balance <= 0:
            return f"Yay! {self.title} project has been funded with {self.pledge_total} worth of pledges!"
        else:
            return f"There's {goal_balance} left to raise until the goal of {self.goal} is reached!"
