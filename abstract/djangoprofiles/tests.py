#-*- coding: utf-8 -*-
import unittest2
from django.db import models
from django.contrib.auth.models import User

from abstract.djangoprofiles.models import UserExtension
from abstract.djangoprofiles.exceptions import MissingAttribute


class ActorsProfileManager(models.Manager):
    def create(self, **kwargs):
        """
        It's all about creation, baby :)
        """
        movies_number = 0
        if isinstance(kwargs['movies_number'], int):
            movies_number = kwargs['movies_number']
        return super(ActorsProfileManager, self).create(
                    user_extension = kwargs['user_extension'], 
                    movies_number = movies_number)


class ActorsProfile(models.Model):
    objects = ActorsProfileManager()
    
    user_extension = models.ForeignKey(UserExtension)
    movies_number = models.IntegerField()
    
    def __unicode__(self):
        return "<Actor Profile for User: %s, %s (%s)> Movies number: %s" % (
                        self.user_extension.surname,self.user_extension.name, 
                        self.user_extension.user.username, self.movies_number)

class DirectorsProfileManager(models.Manager):
    def create(self, **kwargs):
        """
        Again, single method we need
        """
        return super(DirectorsProfileManager, self).create(
                                    user_extension = kwargs['user_extension'], 
                                    company = kwargs.get("company", None))


class DirectorsProfile(models.Model):
    """
    And our second test profile
    """
    objects = DirectorsProfileManager()

    user_extension = models.ForeignKey(UserExtension)
    company = models.CharField(max_length="128")

    def __unicode__(self):
        return "<Director Profile for User: %s, %s (%s)> Company: %s" % (
                        self.user_extension.surname,self.user_extension.name, 
                        self.user_extension.user.username, self.company)

    
class GenericProfileTests(unittest2.TestCase):
    """
    Main test runner
    """
            
    def testActorsProfile(self):
        """
        Here we create Clint Eastwood's profile
        """   
         
        kwargs = {
            "username" : "clienteastwood",
            "name" : "Client",
            "surname" : "Eastwood",
            "password" : "clintpassword",
            "movies_number" : 5,
            "email" : "clint.eastwood@hollywood.com",
            "profile_class" : "%s:%s" % (
                                ActorsProfile.__module__, "ActorsProfile"),
        }        

        user, created = User.objects.create_user(**kwargs)
        assert created    
        assert User.objects.get_profile_info(user)
        

    def testDirectorsProfile(self):
        """
        Can we forget about Stevie ? Hell no !
        """

        kwargs = {
            "username" : "stevenspielberg",
            "name" : "Steven",
            "surname" : "Spielberg",
            "password" : "stevenspielberg",
            "company" : "IL&M, Inc.",
            "email" : "steven.spielberg@ilm.com",
            "profile_class" : "%s:%s" % (
                            DirectorsProfile.__module__, "DirectorsProfile"),
        }  
              
        user, created = User.objects.create_user(**kwargs)
        assert created
        assert User.objects.get_profile_info(user)
        
    def testExceptions(self):
        """
        Let's try to make something with wrong data
        """

        # Let's forget about "username"
        kwargs = {
            "name" : "Steven",
            "surname" : "Spielberg",
            "password" : "stevenspielberg",
            "company" : "IL&M, Inc.",
            "email" : "steven.spielberg@ilm.com",
            "profile_class" : "%s:%s" % (
                            DirectorsProfile.__module__, "DirectorsProfile"),
        }  
        with self.assertRaises(MissingAttribute):
            User.objects.create_user(**kwargs)
            
