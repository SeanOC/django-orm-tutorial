===============
Getting Started
===============

The ORM is an awesome and powerful tool.  It effectively serves a dual role.  First and formost it provides a very easy to use and safe interface to your database saving you from writing tedious CRUD code.  Then it also provides a standard, programatic method for other libraries to understand and work with your database (i.e. `ModelForms <http://docs.djangoproject.com/en/dev/topics/forms/modelforms/#topics-forms-modelforms>`_ or `the Admin <http://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_).

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

Let's create a library.  Open an interactive interpreter session by running:

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


Read
----

On to the thing your applications will be doing the overwhelming majority of the time, reading from the database.

all
~~~

The simplest way we can read from the database is to ask for all of the available instances of a model.  Let's get all of the libraries from the database.

.. code-block:: python

   >>> Library.objects.all()
   [<Library: Library object>, <Library: Library object>]

Pretty easy, right?  We're asking the object manager ``objects`` on the model ``Library`` for ``all``.  The thing returned displays like a list, but it is actually something called a `queryset <http://docs.djangoproject.com/en/dev/ref/models/querysets/#ref-models-querysets>`_.  Querysets are collection type objects which know how to interact with the database in meaningful and relatively efficient ways.  Querysets are also the mechanism by which you create complicated database queries in Django.  We'll talk about them more as we dig more into the ORM.

__unicode__
~~~~~~~~~~~

First, you might have noticed that the output from our call to ``all`` isn't terribly useful.  It tells us that we have two ``Library`` objects, but it doesn't tell us anything about those objects.  To fix this we can add a very simple method to our model

.. code-block:: python

   class Library(models.Model):
       name = models.CharField(max_length=200)
       address = models.CharField(max_length=200)
       state = USStateField()
       phone_number = PhoneNumberField()
       zip_code = models.CharField(max_length=10)
       
   # This is the new bit
   def __unicode__(self):
       return self.name
       
What's this unicode method we've added?  It's a special method, which python uses to know how to represent the object as a unicode string.  The base model class in turn uses that unicode string in it's default ``__repr__`` method.  ``__repr__`` is a special method Python uses to know how to represent the object in places like the interactive shell.

Now that we've defined our ``__unicode__`` method, let's checkout what the results of ``all`` look like now.  First kill your existing shell session by hitting ``ctrl-d`` on unix type systems or ``ctrl-z`` on windows systems.  It is possible to reload modules without restarting your shell but it can lead to some odd states, generally your better off starting with a clean session with each reload.  Now instead of running the same command as before to get an interactive interpreter session, we're going to do something a little different.  Run the following command:

.. code-block:: bash

   (orm-tutorial)user@host:~/tutorial$ ./manage.py shell_plus
   
``shell_plus`` is a management command provided by the ``django_extensions`` app.  It gives you everything that ``shell`` gives you, but it also automatically imports all of your models from all of your installed apps.  This can be a very nice shortcut when your experimenting with model code.

Let's try getting all of the library instances again:

.. code-block:: python

   >>> Library.objects.all()
   [<Library: New York Public Library>, <Library: Seaford Public Library>]
   
Much more useful output!  We can get an idea of which object each entry in the queryset represents.

filter
~~~~~~

Getting all of the libraries is great, but sometimes you just want some of the libraries.  This is where the ``filter`` method comes in.  ``filter`` accepts a series of parameters and returns a queryset of model instances which match the parameters provided.  To get started let's add one more library so we have a bit more data to work with:

.. code-block:: python

   >>> Library.objects.create(name='Public Library of Princeton', address='65 Witherspoon Street', state='NJ', zip_code='08542-3214', phone_number='609-924-9529')
   <Library: Public Library of Princeton>
   
Now, let's do some queries:

.. code-block:: python

   >>> Library.objects.filter(state='NY')
   [<Library: New York Public Library>, <Library: Seaford Public Library>]
   >>> Library.objects.filter(name__startswith='Public')
   [<Library: Public Library of Princeton>]
   >>> Library.objects.filter(name__contains='c')
   [<Library: New York Public Library>, <Library: Seaford Public Library>, <Library: Public Library of Princeton>]
   >>> Library.objects.filter(name__contains='c', state='NY')
   [<Library: New York Public Library>, <Library: Seaford Public Library>]
   >>> Library.objects.filter(name__contains='c').filter(state='NY')
   [<Library: New York Public Library>, <Library: Seaford Public Library>]
   >>> Library.objects.filter(state='CA')
   []
   
In our first query we are asking for all of the libraries who's state is equal to "NY".  Correctly we are returned a queryset with the "New York Public Library" and the "Seaford Public Library".

The second and third queries do something a bit new, it is filtering libraries by name but the ``filter`` parameters have ``__startswith`` and ``__contains`` appended to the end of the field names.  These are called `field lookups <http://docs.djangoproject.com/en/1.1/ref/models/querysets/#id7>`_.  Field lookups provide a simple syntax for doing specific types of queries.

The fourth query has two parameters passed into to filter.  When filter is passed multiple parameters, the conditions of each parameter is connected to the next with an "AND".  More complex queries like "OR" and "NOT" will be covered later.

The fifth query does the same thing as the fourth, it just accomplishes it by "chaining".  The ``filter`` method exists on both manager and queryset classes, accordingly one can call filter multiple time in a "chain" to add more conditions to the query.  Querysets are lazily evaluated (i.e. they don't actually query the database until they absolutely have to) so this can be done without needing to worry about hitting the database each time.

The final query is interesting because it returns an empty queryset.

get
~~~

Get is similar to ``filter`` except that it returns one, and only one instance of the model.  If the provided conditions result in no values or multiple values returned, an exception is raised.  This often can be frustrating for new developers, but it is a very effective way to catch unexpected situations.

Let's use the get method to fetch a single library instance:

.. code-block:: python

   >>> lib = Library.objects.get(name="New York Public Library")
   >>> lib
   <Library: New York Public Library>

Now we have a single library with the name "New York Public Library".  Let's see if all of that library's information is available

.. code-block:: python

   >>> lib.id
   1
   >>> lib.name
   u'New York Public Library'
   >>> lib.address
   u'455 5th Ave'
   >>> lib.state
   u'NY'
   >>> lib.zip_code
   u'10016'
   >>> lib.phone_number
   u'212-222-6559'
   
Now you might be saying "Hold on a second!  Where did that 'id' thing come from?".  All django models are by default, given an automatically incrementing, integer, primary field.  This behavior can be overridden by passing ``primary_key=True`` as a parameter to any explicitly defined field which you wish to have act as the primary key.

get_or_create
~~~~~~~~~~~~~

One last trick up the ORM's sleeve: there's a convience method called ``get_or_create``.  As the name suggests it will try to find an object with the parameters you provide and if it cannot find one, it will create one.

.. code-block:: python

   >>> lib, created = Library.objects.get_or_create(name='Public Library of Princeton', defaults={'addres': '65 Witherspoon Street', 'state': 'NJ', 'zip_code': '08542-3214', 'phone_number': '609-924-9529',})
   >>> lib
   <Library: Public Library of Princeton>
   >>> created
   False
   >>> lib, created = Library.objects.get_or_create(name='Denver Public Library', defaults={'address': '10 W 14th Avenue Pkwy', 'state': 'CO', 'zip_code': '80204', 'phone_number': '720-865-1111',})
   >>> lib
   <Library: Denver Public Library>
   >>> created
   True
   
``get_or_create`` accepts a series of parameters and a dictionary called ``defaults``.  The parameters will be used for querying and creation while ``defaults`` will only be used to populate fields when creating a new object.  The method returns a tuple containing the new object and a boolean value reflecting weather or not that object has just been created.

Update
------

So now we're creating objects, sticking them in the database, and fetching them back.  How do we update the values on objects which we've already created?

To start we need to get an object to work with:

.. code-block:: python
   
   >>> lib = Library.objects.get(name="New York Public Library")
   >>> lib
   <Library: New York Public Library>
   
Now let's say that the library has switched to a fancy new "800" number, we need to update our database:

.. code-block:: python

   >>> lib.phone_number
   u'212-222-6559'
   >>> lib.phone_number = '800-nyc-books'
   >>> lib.save()
   >>> lib.phone_number
   '800-nyc-books'
   
Here we are modifying our object in python, and then calling the ``save`` method on it.  If we do not call the save method, the change does not get persisted to the database.  To prove that our change actually has updated our database, you can go and query your database directly or you can run the query again within django:

.. code-block:: python

   >>> lib = None
   >>> lib
   >>> lib = Library.objects.get(name="New York Public Library")
   >>> lib
   <Library: New York Public Library>
   >>> lib.phone_number
   u'800-nyc-books'
   >>>
   
You can also perform updates in bulk across a queryset:

.. code-block:: python

   >>> ny_libraries = Library.objects.filter(state='NY')
   >>> ny_libraries
   [<Library: New York Public Library>, <Library: Seaford Public Library>]
   >>> ny_libraries[0].phone_number
   u'800-nyc-books'
   >>> ny_libraries[1].phone_number
   u'516-221-1334'
   >>> ny_libraries.update(phone_number='800-NYS-BOOKS')
   2
   >>> ny_libraries = Library.objects.filter(state='NY')
   >>> ny_libraries
   [<Library: New York Public Library>, <Library: Seaford Public Library>]
   >>> ny_libraries[0].phone_number
   u'800-NYS-BOOKS'
   >>> ny_libraries[1].phone_number
   u'800-NYS-BOOKS'
   
Here you can see that we query for all of the libraries in NY and update their phone number to '800-NYS-BOOKS'.  Be aware that there is a gotcha with using this method.  It is a very efficient way to preform bulk updates since the update is performed with a single database query, it also avoids ever calling the ``save`` method or triggering the ``pre_save`` and ``post_save`` signals.  With a stock django model this isn't a problem but if you have added code which depends on any of those getting called whenever an object is modified, you can end up in trouble.

Delete
------

Finally we're up to taking stuff out of the database.  At this point, you can probably guess how things are going to go:

.. code-block:: python

   >>> lib = Library.objects.get(name='Denver Public Library')
   >>> lib
   <Library: Denver Public Library>
   >>> lib.delete()
   >>> lib = Library.objects.get(name='Denver Public Library')
   Traceback (most recent call last):
     File "<console>", line 1, in <module>
     File "/Users/user/.virtualenvs/orm-tutorial/src/django/django/db/models/manager.py", line 132, in get
       return self.get_query_set().get(*args, **kwargs)
     File "/Users/user/.virtualenvs/orm-tutorial/src/django/django/db/models/query.py", line 339, in get
       % self.model._meta.object_name)
   DoesNotExist: Library matching query does not exist.
   >>> ny_libraries = Library.objects.filter(state='NY')
   >>> ny_libraries
   [<Library: New York Public Library>, <Library: Seaford Public Library>]
   >>> ny_libraries.delete()
   >>> ny_libraries = Library.objects.filter(state='NY')
   >>> ny_libraries
   []
   
Just like updates, you can call ``delete`` on a model instance to delete the individual model, or you can call ``delete`` on a queryset.  Again like before, calling ``delete`` on a queryset is efficient but it does not call the ``delete`` method on the individual model instances nor does it trigger the ``pre_delete`` or ``post_delete`` signals.

Relations
=========

As the term "relational database" suggests, a major component of schema design is relating one "model" to another.  Django offers some solid tools for creating, using, and managing the most common types of relationships found in relational databases.

One to many
-----------

Foreign keys or one to many relationships are the most common type of relationship found in relational databases.  Let's create a new model which connects to our ``Library`` model via a foreign key.  In ``library/models.py`` add the following after your ``Library`` model:

.. code-block:: python

   class Patron(models.Model):
       name = models.CharField(max_length=200)
       library = models.ForeignKey(Library)
       
       def __unicode__(self):
           return name

Our foriegn key field looks like any other field except that it takes the class of the model to be linked to as a parameter.  Alternatively you can pass a string with the format ``'<app_name>.<model_name>'``, this allows you to work around potential circular dependencies.

Now we need to run ``syncdb`` again to create our new table:

.. code-block:: bash

   (orm-tutorial)user@host:~/tutorial$ ./manage.py syncdb
   Creating table library_patron
   Installing index for library.Patron model
   
Assuming your database supports doing so, you should be able to look at your database now to see the new table including a foreign key constraint to the ``library_library`` table.

Let's fire up our shell again using ``./manage.py shell_plus`` and create some related entries:

.. code-block:: python

   >>> lib = Library.objects.all()[0]
   >>> lib
   <Library: Public Library of Princeton>
   >>> p = Patron.objects.create(name='Bob Smith', library=lib)
   >>> p
   <Patron: Bob Smith>
   >>> p2 = Patron.objects.create(name='Jane Doe', library=lib)
   >>> p2
   <Patron: Jane Doe>
   
We've now created two patrons of the Princeton library.  Thanks to the way Django's ORM is setup, we can now access information both ways across that relationship:

.. code-block:: python
   
   >>> p.library
   <Library: Public Library of Princeton>
   >>> p2.library
   <Library: Public Library of Princeton>
   >>> lib.patron_set.all()
   [<Patron: Bob Smith>, <Patron: Jane Doe>]
   
Here you can see that accessing the ``library`` attribute on each of the patrons returns the full, related library object.  Similarly, the ``patron_set`` attribute of the library object allows us to query the reverse side of the relationship.  The name of the attribute ``patron_set`` is automatically selected by Django.  By default the reverse access property for a foreign key will always be ``<model_name>_set``.  This can be overridden by passing a ``related_name`` parameter to the foreign key's definition.

One to one
----------

One to one fields are almost the same as foreign keys but they are a bit more restricted and have a slightly simpler API.  As their name suggests, one to one relationships are exclusive.  Once an instance of one model has related to an instance of another model using a one to one field, no other instance of the first model may make the same relationship.  Let's add another model to our library app so that we can play with this:

.. code-block:: python
   
   class Librarian(models.Model):
       name = models.CharField(max_length=200)
       library = models.OneToOneField(Library)

       def __unicode__(self):
           return self.name
           
Once again, we need to run ``syncdb`` and restart our shell.

Now let's work with our new model a bit:

.. code-block:: python

   >>> lib = Library.objects.all()[0]
   >>> 
   >>> lib
   <Library: Public Library of Princeton>
   >>> librarian = Librarian.objects.create(name='Philip J. Fry', library=lib)
   >>> librarian
   <Librarian: Philip J. Fry>
   >>> librarian.library
   <Library: Public Library of Princeton>
   >>> lib.librarian
   <Librarian: Philip J. Fry>
   
Here you can see that accessing the relationship is very easy.  As expected accessing the library attribute on the librarian returned the library instance.  Similarly a librarian property is now available on the library object and accessing that property returns a librarian instance.  By default the reverse property name is based on the model name.  Again like with foreign keys, the value of the reverse property can be set by passing a ``related_name`` argurment to the ``OneToOneField`` definition.  

Finally notice what happens if we try to create another librarian with the same library property set.

.. code-block:: python

   
   >>> librarian = Librarian.objects.create(name='Hermes Conrad', library=lib)
   Traceback (most recent call last):
     File "<console>", line 1, in <module>
     File "/Users/user/.virtualenvs/orm-tutorial/src/django/django/db/models/manager.py", line 138, in create
       return self.get_query_set().create(**kwargs)
     File "/Users/user/.virtualenvs/orm-tutorial/src/django/django/db/models/query.py", line 350, in create
       obj.save(force_insert=True, using=self.db)
     File "/Users/user/.virtualenvs/orm-tutorial/src/django/django/db/models/base.py", line 430, in save
       self.save_base(using=using, force_insert=force_insert, force_update=force_update)
     File "/Users/user/.virtualenvs/orm-tutorial/src/django/django/db/models/base.py", line 519, in save_base
       result = manager._insert(values, return_id=update_pk, using=using)
     File "/Users/user/.virtualenvs/orm-tutorial/src/django/django/db/models/manager.py", line 195, in _insert
       return insert_query(self.model, values, **kwargs)
     File "/Users/user/.virtualenvs/orm-tutorial/src/django/django/db/models/query.py", line 1432, in insert_query
       return query.get_compiler(using=using).execute_sql(return_id)
     File "/Users/user/.virtualenvs/orm-tutorial/src/django/django/db/models/sql/compiler.py", line 789, in execute_sql
       cursor = super(SQLInsertCompiler, self).execute_sql(None)
     File "/Users/user/.virtualenvs/orm-tutorial/src/django/django/db/models/sql/compiler.py", line 733, in execute_sql
       cursor.execute(sql, params)
     File "/Users/user/.virtualenvs/orm-tutorial/src/django/django/db/backends/util.py", line 19, in execute
       return self.cursor.execute(sql, params)
     File "/Users/user/.virtualenvs/orm-tutorial/src/django/django/db/backends/sqlite3/base.py", line 193, in execute
       return Database.Cursor.execute(self, query, params)
   IntegrityError: column library_id is not unique
   
Since there is already a librarian with that library assigned, the unique constraint created with the ``OneToOneField`` prevents the new librarian from being created.

Many To Many
------------

The final type of common relationship found in relational databases is the many to many.  Here an intermediary table sits between two primary tables and keeps track of relationships between the two tables.  Let's add one last model for us to play with:

.. code-block:: python

   class Book(models.Model):
       title = models.CharField(max_length=200)
       libraries = models.ManyToManyField(Library)

       def __unicode__(self):
           return self.title

And again, we need to run ``syncdb`` and restart our shell.  

.. code-block:: bash

   (orm-tutorial)user@host:~/tutorial$ ./manage.py syncdb
   Creating table library_book_libraries
   Creating table library_book
   Installing index for library.Book_libraries model

Notice that when you ran ``syncdb``, two tables were created.  The ``library_book`` table represents the actual ``Book`` model while the ``library_book_libraries`` table handles the relationships between books and libraries.

Let's create some instances of our new model so we can play with the many to many relationship:

.. code-block:: python

   >>> b1 = Book.objects.create(title="The Hitchhiker's Guide to the Galaxy")
   >>> b2 = Book.objects.create(title="The Restaurant at the End of the Universe")
   >>> b3 = Book.objects.create(title="So Long, and Thanks for All the Fish")
   >>> b1
   <Book: The Hitchhiker's Guide to the Galaxy>
   >>> b2
   <Book: The Restaurant at the End of the Universe>
   >>> b3
   <Book: So Long, and Thanks for All the Fish>
   
   
OK, we have some books now.  Notice however that they are not related to anything yet.  Since many to many relationships work via an intermediary table, we need to create all of our objects before we can define any relationships.

Let's fetch some libraries to play with:

.. code-block:: python

   >>> lib1 = Library.objects.all()[0]
   >>> lib2 = Library.objects.create(name="New York Public Library", address='455 5th Ave', state='NY', zip_code='10016', phone_number='212-222-6559')
   
add
~~~

Now let's add some books to some libraries:

.. code-block:: python

   >>> lib1.book_set.add(b1)
   >>> lib1.book_set.add(b2)
   >>> lib2.book_set.add(b3)
   >>> lib2.book_set.add(b1)
   >>> lib1.book_set.all()
   [<Book: The Hitchhiker's Guide to the Galaxy>, <Book: The Restaurant at the End of the Universe>]
   >>> lib2.book_set.all()
   [<Book: So Long, and Thanks for All the Fish>, <Book: The Hitchhiker's Guide to the Galaxy>]
   >>> b1.libraries.all()
   [<Library: Public Library of Princeton>, <Library: New York Public Library>]
   >>> b2.libraries.all()
   [<Library: Public Library of Princeton>]
   >>> b3.libraries.all()
   [<Library: New York Public Library>]
   >>> b3.libraries.add(lib1)
   >>> lib1.book_set.all()
   [<Book: The Hitchhiker's Guide to the Galaxy>, <Book: The Restaurant at the End of the Universe>, <Book: So Long, and Thanks for All the Fish>]
   
So to summarize what's going on above:  the ``Book`` class has an attribute called ``libraries`` and the ``Library`` class has an attribute called ``book_set``.  These each offer an interface into the ManyToMany relationship of the two models.  By calling ``add`` on either interface and passing an instance of the opposite model, a relationship is formed between the two.  By default these relationships are symmetrical.  That behavior can be changed when defining the `ManyToManyField <http://docs.djangoproject.com/en/dev/ref/models/fields/#manytomanyfield>`_ as well as the ``related_name`` and the model which the relationship goes through.

remove
~~~~~~

Remove works pretty much the same as add:

.. code-block:: python

   >>> lib1.book_set.remove(b1)
   >>> lib1.book_set.all()
   [<Book: The Restaurant at the End of the Universe>, <Book: So Long, and Thanks for All the Fish>]
   >>> b1.libraries.all()
   [<Library: New York Public Library>]
   >>> b3.libraries.all()
   [<Library: Public Library of Princeton>, <Library: New York Public Library>]
   >>> b3.libraries.remove(lib1)
   >>> b3.libraries.all()
   [<Library: New York Public Library>]
   >>> lib1.book_set.all()
   [<Book: The Restaurant at the End of the Universe>]
   
clear
~~~~~

Clear can be called from either end of a relationship and removes all of the relations to an object:

.. code-block:: python

   >>> lib2.book_set.all()
   [<Book: So Long, and Thanks for All the Fish>, <Book: The Hitchhiker's Guide to the Galaxy>]
   >>> lib2.book_set.clear()
   >>> lib2.book_set.all()
   []
   >>> b1.libraries.all()
   []
   
Conclusion
==========

So that's it for basic ORM functionality.  From here you should be able to build most basic applications and move on to learn about more advanced bits of the ORM.

You can get the source to these docs as well as the completed example project at `github <http://github.com/SeanOC/django-orm-tutorial>`_.