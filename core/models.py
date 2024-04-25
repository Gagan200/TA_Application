from django.db import models
from django.utils import timezone
from accounts.models import UserAccount

class Course(models.Model):
    position = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self) -> str:
        return self.position


class Application(models.Model):
    SUBMITTED = "SUBMITTED"
    RECOMMENDED = "RECOMMENDED"
    APPROVED = "APPROVED"
    DISAPPROVED = "DISAPPROVED"

    STATUS_CHOICES = (
        (SUBMITTED, "Submitted"),
        (RECOMMENDED, "Recommended"),
        (APPROVED, "Approved"),
        (DISAPPROVED, "Disapproved"),
    )

    user = models.ForeignKey("accounts.UserAccount",on_delete=models.CASCADE)
    course = models.ForeignKey("core.Course", on_delete=models.CASCADE)
    cv1 = models.FileField(upload_to="CVs/", max_length=100)
    cv2 = models.FileField(upload_to="CVs/", max_length=100, null=True, blank=True)
    cv3 = models.FileField(upload_to="CVs/", max_length=100, null=True, blank=True)
    cv4 = models.FileField(upload_to="CVs/", max_length=100, null=True, blank=True)
    certificate1 = models.FileField(upload_to="CVs/", max_length=100, null=True, blank=True)
    certificate2 = models.FileField(upload_to="CVs/", max_length=100, null=True, blank=True)
    certificate3 = models.FileField(upload_to="CVs/", max_length=100, null=True, blank=True)
    certificate4 = models.FileField(upload_to="CVs/", max_length=100, null=True, blank=True)

    # Checklist
    box1 = models.BooleanField(default=False)
    box2 = models.BooleanField(default=False)
    box3 = models.BooleanField(default=False)
    box4 = models.BooleanField(default=False)
    box5 = models.BooleanField(default=False)
    box6 = models.BooleanField(default=False)
    box7 = models.BooleanField(default=False)
    box8 = models.BooleanField(default=False)

    recommended = models.BooleanField(default=False)
    has_experience = models.BooleanField()
    message = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default=SUBMITTED, max_length=15)

    approved_by = models.ManyToManyField("accounts.UserAccount", related_name="approved_applications", blank=True)
    disapproved_by = models.ManyToManyField("accounts.UserAccount", related_name="disapproved_applications", blank=True)

    liked_by = models.ManyToManyField("accounts.UserAccount", related_name="liked_applications", blank=True)
    disliked_by = models.ManyToManyField("accounts.UserAccount", related_name="disliked_applications", blank=True)

    def check_or_decide_result(self):
        # Finallise if every commitee member has voted
        total_members = UserAccount.objects.filter(user_type=UserAccount.COMMITTEE_MEMBER, is_verified_user=True).count()
        members_voted = self.approved_by.count() + self.disapproved_by.count()

        if ( members_voted >= total_members ):
            if self.approved_by.count() > self.disapproved_by.count():
                self.status = self.APPROVED
            else:
                self.status = self.DISAPPROVED

    def approve_by(self, user):
        if (user in self.approved_by.all() or user in self.disapproved_by.all()):
            return  # already voted
        if (user.user_type != UserAccount.COMMITTEE_MEMBER): 
            return  # user must be a Committee member
        
        self.approved_by.add(user)
        self.check_or_decide_result()
        self.save()

    def disapprove_by(self, user):
        if (user in self.approved_by.all() or user in self.disapproved_by.all()):
            return  # already voted
        if (user.user_type != UserAccount.COMMITTEE_MEMBER): 
            return  # user must be a Committee member
        
        self.disapproved_by.add(user)
        self.check_or_decide_result()
        self.save()

    def like_by(self, user):
        if (user in self.liked_by.all() or user in self.disliked_by.all()):
            return  # already voted
        if (user.user_type != UserAccount.INSTRUCTOR): 
            return  # user must be a Committee member
        
        self.liked_by.add(user)
        self.save()
        
    def dislike_by(self, user):
        if (user in self.liked_by.all() or user in self.disliked_by.all()):
            return  # already voted
        if (user.user_type != UserAccount.INSTRUCTOR): 
            return  # user must be a Committee member
        
        self.disliked_by.add(user)
        self.save()
    
        
class Comment(models.Model):
    user = models.ForeignKey("accounts.UserAccount", on_delete=models.CASCADE)
    application = models.ForeignKey("core.Application", on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date = timezone.now()

        return super(Comment, self).save(*args, **kwargs)
