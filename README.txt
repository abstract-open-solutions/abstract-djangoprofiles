Introduction
============

The point here is to give the chance to associate different Django profiles to
Users.

Picture a scenario where you have two profiles, ``Customer`` and ``Business``,
respectively described from the following information:


Customer:

- username
- name
- surname
- Role

Business

- username
- name
- surname
- Company

 and suppose your site has two different forms to get the data from the users.
 
This package stores the data shared between the two different profiles into 
``UserExtension`` model, and tries to use the correct model to store the 
specific ones.

In our example, ``username`` is a standard field from standard ``User`` model, 
while name and surname are shared data, and Role and Company are specific ones.

The system supposes to be supplied with two models, e.g.: ``BusinessProfile``
and ``CustomerProfile``, that have to respect a single constraint:

. they have to store a foreign key to ``UserExtension`` model

If all this happens, the process is the following:

. ``User`` object is created
. an event is fired, and the binded handler creates:
  - the ``UserExtension`` object
  - the specifi profile object
  
At this point, just using "get_profile_info" onto a User object, lets user
obtain the specific profile object with all the data into it.