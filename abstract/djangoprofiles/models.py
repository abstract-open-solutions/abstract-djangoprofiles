#-*- coding: utf-8 -*-
import importlib
from django.dispatch import receiver, Signal
from django.db import models
from django.contrib.auth.models import User, UserManager

from abstract.djangoprofiles.exceptions import MissingAttribute

class UserExtensionManager(models.Manager):
    """
    """
    
    def extension_class(self, extension):
        """
        """
        
        module, klass = extension.split(':',1)        
        klass=getattr(importlib.import_module(module), klass)
        
        return klass
        
    
    def create(self, **kwargs):
        """
        Here i can suppose to receive:
        user - the user extension is related to
        name - guess what
        surname - can't remember...
        profile_class: something like module:Class
            such an information will be stored into settings file (meh...)
        """
        if not kwargs['name']:
            raise MissingAttribute("name")
            
        if not kwargs['surname']:
            raise MissingAttribute("surname")                    
            
        if not kwargs['profile_class']:
            raise MissingAttribute("profile_class")

        if not kwargs['username']:
            raise MissingAttribute("username")

        if not kwargs['password']:
            raise MissingAttribute("password")

        if not kwargs['user']:
            raise MissingAttribute("user")
    
        klass=self.extension_class(kwargs['profile_class'])
                
        
        # XXX This deserve a better handler - what is an exception is 
        # fired ?
        user_extension = UserExtension( user = kwargs['user'],
                                    name = kwargs['name'],
                                    surname = kwargs['surname'],
                                    profile_class = kwargs['profile_class'],
                                    )
                                    
        user_extension.save()
            
        try:
            specific_profile = klass.objects.create(
                                    user_extension = user_extension,
                                    **kwargs)
        except:
            user_extension.delete()
            return specific_profile, False
        
        return specific_profile, True
        
    def get_profile_info(self, user):
        """
        """
        
        if not user:
            raise MissingAttribute("user")
            
        obj = super(UserExtensionManager, self).get(user = user)
        
        klass = self.extension_class(obj.profile_class)
        return klass.objects.get(user_extension = obj)
        
        
    
class UserExtension(models.Model):
    """
    """
    
    objects  = UserExtensionManager()
    
    user = models.ForeignKey(User)
    
    name = models.CharField(max_length = 64)
    surname = models.CharField(max_length = 64)
    profile_class = models.CharField(max_length = 128)
    

# This signal will be fired once the user object will be saved
user_created = Signal(providing_args=["username", ])

@receiver(user_created, sender=User)
def newuser_handler(**kwargs):
    """
    """
    # Not nice, but that's it
    kwargs['user'] = kwargs['instance']
    UserExtension.objects.create(**kwargs)
    
class ExtendedUserManager(UserManager):
    """
    """
        
    def get_profile_info(self, user):
        """
        """
        user_profile = UserExtension.objects.get_profile_info(user)
        return user_profile
        
    def create_user(self, **kwargs):
        """
        """
        username = kwargs.get("username", None)
        email = kwargs.get("email", None)
        password = kwargs.get("password",None)
        
        if not username:
            raise MissingAttribute("username")
            
        if not email: 
            raise MissingAttribute("email")
            
        if not password:
            raise MissingAttribute("password")
        
        try:
            user_object = super(ExtendedUserManager, self).create_user(
                                username=username, 
                                password=password, 
                                email=email)
            user_created.send(sender=User, instance=user_object, **kwargs)
            return user_object,True
        except:
            return None, False

User.objects = ExtendedUserManager()
User.objects.model = User