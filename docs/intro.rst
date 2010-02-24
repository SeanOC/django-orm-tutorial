===============
Getting Started
===============

The ORM is an awesome and powerful tool.  It effectively serves a dual role.  First and formost it provides a very easy to use and safe interface to your database saving you from writing tedious CRUD code.  Then it also provides a standard, programatic method for other libraries to understand and work with your database (i.e. `ModelForms <http://docs.djangoproject.com/en/dev/topics/forms/modelforms/#topics-forms-modelforms>`_).

Project Setup
=============

To get started, let's create a new django project and an application within that project.

.. code-block:: bash

   (orm-tutorial)user@host:~$ django-admin.py startproject tutorial
   (orm-tutorial)user@host:~$ cd tutorial
   (orm-tutorial)user@host:~/tutorial$ ./manage.py startapp library
   
Now that your project and application has been stubbed out, open ``settings.py`` and enter your database `settings <http://docs.djangoproject.com/en/dev/ref/settings/#database-engine>`_.  Feel free to use sqlite or the database of your choice for this tutorial.  While your settings file is open you will also want to add ``'django_extensions',`` to you list of installed apps.  While django-extensions isn't strictly required, it does offer a number of tools which will be helpful throughout the tutorial.

Models
======

Once your database settings are in place, let's define our first model.  Open ``library/models.py`` for editing and add a model for a library (i.e. the building which holds books).

.. code-block:: python

   from django.db import models
   from django.contrib.localflavor.us.models import USStateField, PhoneNumberField

   class Library(models.Model):
       name = models.CharField(max_length=200)
       address = models.CharField(max_length=200)
       state = USStateField()
       phone_number = PhoneNumberField()
       zip_code = models.CharField(max_length=10)
       
Congratulations!  You now have your first model.  With this tiny bit of code, you now are able to create, update, delete, and query for libraries in your database.  Let's pause for a second and take a look at what's going on here.

.. code-block:: python

   from django.db import models
   from django.contrib.localflavor.us.models import USStateField, PhoneNumberField
   
These are the imports required for our model.  Generally the ``models`` class is all you need, but we wanted to bring in some specialized fields.  We'll talk a bit more about ``USStateField`` and ``PhoneNumberField`` later.

.. code-block:: python

   class Library(models.Model):
   
Here we are declaring the class for our Model.  It inherits from the base ``Model`` class.  The base ``Model`` class is what gives us all of the out-of-the-box functionality and allows such a little block of code to be so powerful.

.. code-block:: python

   name = models.CharField(max_length=200)
   
Next we add an attribute to the model called name.  By assigning a CharField object to that attribute, we're telling the ORM what our schema should look like as well as how it should validate data coming into out model.  In most database backends, ``models.CharField`` translates to a ``varchar`` field.  Notice the ``max_length`` argument passed into the CharField declaration; this is a required argument which, as its name suggests, sets a limit on the length of possible values.
