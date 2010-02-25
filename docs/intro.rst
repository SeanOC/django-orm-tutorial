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
   
Now that your project and application has been stubbed out, open ``settings.py`` and enter your database `settings <http://docs.djangoproject.com/en/dev/ref/settings/#database-engine>`_.  Feel free to use sqlite or the database of your choice for this tutorial.  While your settings file is open you will also want to add ``'django_extensions',`` and ``'library',`` to you list of installed apps.  Django-extensions isn't strictly required, it does offer a number of tools which will be helpful throughout the tutorial.

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

.. code-block:: python

   state = USStateField()
   phone_number = PhoneNumberField()
   
These are some specialized fields.  Under the covers they are just just char fields with some extra validation applied to them.  You should also notice that for these fields we are just using the classes we imported and we're not saying ``models.``.  Often it will be useful to use existing specialized fields or even create your own.

.. code-block:: python

   zip_code = models.CharField(max_length=10)
   
Finally we declare the zipcode field.  The choice of type for this field may see odd at first glance but it is not an accident.  While technically zip codes are 5 or 9 digit numbers (`zip+4 <http://en.wikipedia.org/wiki/ZIP_code#ZIP_.2B_4>`_), we care more about the formatting and display of those digits than their actual numeric value.  We'll never do math with a zipcode but we do care if we loose leading zeros.

Create Database
===============

Now that we've defined our schema in code, we need to create an actual database.  In your shell, run the following command:

.. code-block:: bash

   (orm-tutorial)user@host:~/tutorial$ ./manage.py syncdb
   
You will see the command creating several tables, including your library table.  At some point it will prompt you if you want to create a superuser, feel free to say no to this as we will not be using it in this tutorial.

If your interested, take a minute to poke around in the database which has just been created.  In particular check out the ``library_library`` table.  By default Django will create tables using a ``<app_name>_<model_name>`` pattern.  This is done to avoid name collisions across applications.  If you wish to have a different name or work with a table from a legacy database, you can change the table a model will use via `meta options <http://docs.djangoproject.com/en/dev/ref/models/options/#ref-models-options>`_.

CRUD
====

Create, read, update, and delete; these are the fundamental operations any database driven application needs to perform.  Now that we've created a model class, we have all the tools needed to perform all of these operations in an easy and safe way.

Create
------

Let's create a library.  Open an interactive interpreter session by running ``./manage.py shell_plus``.  ``shell``.

.. code-block:: bash

   (orm-tutorial)user@host:~/tutorial$ ./manage.py shell
   
You will get a prompt like this

.. code-block:: python

   Python 2.6.4 (r264:75706, Dec 21 2009, 20:20:53) 
   [GCC 4.0.1 (Apple Inc. build 5493)] on darwin
   Type "help", "copyright", "credits" or "license" for more information.
   (InteractiveConsole)
   >>>
   
You now have an interactive interpreter session.  This is a very powerful tool which languages like Python offer.  The interactive interpreter lets you very easily experiment with your code and get immediate feedback.  Now let's get back to creating that library

.. code-block:: python

   >>> from library.models import Library
   >>> lib = Library(name="New York Public Library", address='455 5th Ave', state='NY', zip_code='10016', phone_number='212-222-6559')
   >>> lib.save()
   
We imported the ``Library`` model class, created an instance with some initial values and then saved that to the database.  Alternatively we can combine the last two steps by using the ``create`` method.

.. code-block:: python

   >>> lib2 = Library.objects.create(name='Seaford Public Library', address='2234 Jackson Ave', state='NY', zip_code='11783', phone_number='516-221-1334')
   
If you now go look at your database, you'll find two rows have been added with the information above.
