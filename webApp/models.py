from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import json


# Create your models here.

# Model of tags
class Tag(models.Model):
    symbol = models.CharField(primary_key=True, max_length=10)
    short_name = models.CharField(max_length=20, null=True)
    debt_equ = models.FloatField(default=0)
    insiders = models.FloatField(default=0)
    price = models.FloatField(default=0)
    t_price = models.FloatField(default=0)
    upside = models.FloatField(default=0)
    t_pe = models.FloatField(default=0)
    f_pe = models.FloatField(default=0)
    t_eps = models.FloatField(default=0)
    f_eps = models.FloatField(default=0)
    roa = models.FloatField(default=0)
    roe = models.FloatField(default=0)
    profit_m = models.FloatField(default=0)
    my_score = models.FloatField(default=0)
    my_count = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["symbol"]

    def __str__(self) -> str:
        return self.symbol

# Model of categories


class Category(models.Model):
    name = models.CharField(
        primary_key=True, max_length=80, verbose_name="name_category")
    associated_tags = models.CharField(max_length=5000, default="[]")

    @property
    def associated_tags_list(self):
        return json.loads(self.associated_tags)

    @associated_tags_list.setter
    def associated_tags_list(self, list):
        self.associated_tags_list = json.dumps(list)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

# Model of profiles to store the sesion information of a user


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    associated_tags = models.ManyToManyField(
        Tag, verbose_name="Tags", blank=True)
    associated_categories = models.ManyToManyField(
        Category, verbose_name="Categories", blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["-id"]

# Method that creates a profile associated to a user(instance) on call


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Method that saves the user's info into the profile on call


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Statements to call both functions just after an user is created
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
