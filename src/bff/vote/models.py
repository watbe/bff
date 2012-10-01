from django.db import models

# Create your models here.

class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Menu(models.Model):
    date = models.DateField(editable=True, unique=True)

    def __unicode__(self):
        return self.date.strftime("%d %b %y") #Format corresponds to 28 Sep 12


class Meal(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    menu = models.ForeignKey(Menu)

    def __unicode__(self):
        return self.name


VOTE_CHOICES = (
    (0, 'Unsatisfactory'),
    (1, 'Satisfactory'),
    (2, 'Great'),
)

class Vote(models.Model):
    meal = models.ForeignKey(Meal)
    rating = models.SmallIntegerField(choices=VOTE_CHOICES, null=True)

class VoteEvent(models.Model):
    class Meta:
        unique_together = ('room_number', 'menu')

    room_number = models.CharField(max_length=4)
    menu = models.ForeignKey(Menu)

