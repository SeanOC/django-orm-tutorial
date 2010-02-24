=====
Setup
=====

To get started you will need to take a few steps to get your environment setup.  The steps described below are slightly more involved than strictly needed to get going, but they do follow best practices for virtually all python development.

Install Environment Tools
=========================

There are a few tools you will need to install and manage python packages.  We are assuming that you have already installed `python <http://python.org>`_ on your system.

pip
---

`pip <http://pip.openplans.org/>`_ is a modern replacement for easy_install.  It offers a variety of useful features including the ability to uninstall packages and the ability to install packages from source control repositories.

If you have setuptools installed you can simply do:

.. code-block:: bash

   user@host:~$ easy_install pip
   
Otherwise you can download pip.py and run it directly. Alternatively you can download it from `pypi <http://pypi.python.org/pypi/pip>`_ and install it by extracting the package, navigating to the directory in your shell and running the command:

.. code-block:: bash

   user@host:~$ python setup.py install
   
virtualenv
----------

`virtualenv <http://pypi.python.org/pypi/virtualenv>`_ is a tool which allows you to install packages into a specific "environment" instead of your global site-packages.  This allows you to have multiple versions of a given package on your system and it allows you to more easily replicate environments across systems.

To install virtualenv run the following command:

.. code-block:: bash

   user@host:~$ pip install virtualenv
   
virtualenvwrapper (unix type systems only)
------------------------------------------

If you are on a system like Linux or or OS X, you will also want to install a tool called `virtualenvwrapper <http://www.doughellmann.com/projects/virtualenvwrapper/>`_.  virtualenvwrapper adds some tools to your shell to make working with virtual environments much easier.  If you are on Windows this tool won't be terribly helpful and you shouldn't install it.

To install virtualenv wrapper run the following command:

.. code-block:: bash

   user@host:~$ pip install virtualenvwrapper
   
Once installed you need create a directory to hold your virtualenvs.  Most people use ``~/.virtualenvs`` but you can make it what ever you like.

Next you will need to add three entries to your shell init file.  Depending on your system, this file will be called something like ``~/.profile``, ``~/.bashrc``, or ``~/.bash_profile``.  The two lines to add are below:

.. code-block:: bash

   export WORKON_HOME=$HOME/.virtualenvs
   export PIP_VIRTUALENV_BASE=$WORKON_HOME
   source /usr/local/bin/virtualenvwrapper_bashrc
   
Here ``WORKON_HOME`` should be the full path to the directory you just created and the second line should be the path to the ``virtualenvwrapper_bashrc`` file which was installed when you installed virtualenvwrapper.  The first two entries tell virtualenv and pip where to find/put your virtual envs.  The last entry loads a bunch of utility commands to make it easier to work with virtualenvs.

Finally you need to load these changes into your active environment.  Run the command below with what ever your shell init file's path in place of ``~/.profile``:

.. code-block:: bash

   user@host:~$ source ~/.profile
   
Now you should have all of the basic tools you'll need to setup your python project.

Environment Setup
=================

Now we're going to create your virtual environment and install all of the packages you will need for the tutorial.  

Create a virtual environment
----------------------------

As explained before, virtualenv allows us to install packages to specific environments instead of our global python path.  To take advantage of this you will need to create a new virtual environment for your project.  Below there are two sections; if you installed virtualenvwrapper follow the first, if not follow the second.

With virtualenvwrapper (unix type systems)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   user@host:~$ mkvirtualenv orm-tutorial

You have now created a virtual environment and activated that environment.  Your shell prompt should now include a bit which looks like ``(orm-tutorial)``.  This lets you know which environment you currently have active.  Any python scripts you run will load packages from your virtualenv and any packages you install will get installed to the virtual env.  When you are done working on this project you should run the command below:

.. code-block:: bash
   
   user@host:~$ deactivate
   
This will deactivate your virtualenv.  Once you've run this command, scripts will only look in your global python path for packages and anything you install will go into your global site-packages directory.  When your ready to come back to this project run the following command:

.. code-block:: bash

   user@host:~$ workon orm-tutorial
   
This will activate an existing virtualenv.  On most systems, you are able to use tab completion to help select the virtualenv you'd like to use.

Without virtualenvwrapper (Windows)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First you will need to create a directory where you'd like to keep your virtual environments.  Usually it will make sense for this to be some place along side where ever you keep your python projects.  Once the directory has been created you will need to create your virtualenv using the command below: ::

   C:\> virtualenv \path\to\virtualenvs\dir\orm-tutorial
   
Here the path before ``orm-tutorial`` should be the directory you just created.  Now that you've created your virtualenv, you need to activate it: ::

   C:\> \path\to\virtualenvs\dir\orm-tutorial\Scripts\activate.bat
   
This has activated your virtual env.  When you are done you will want to call the ``deactivate`` command to deactivate your virtualenv.  When you come back to work on this project, you will want to run the command above again to activate your virtualenv.

Get Tutorial Source
===================

Make sure you have `git <http://git-scm.com/>`_ installed.  Once you do check out the tutorial with the command:

.. code-block:: bash

   (orm-tutorial)user@host:~$ git checkout git://github.com/SeanOC/django-orm-tutorial.git
   
Install Dependencies
====================
   
Go into the tutorial directory

.. code-block:: bash

   (orm-tutorial)user@host:~$ cd django-orm-tutorial
   
Install the project dependencies using pip

.. code-block:: bash

   (orm-tutorial)user@host:~$ pip install -Ir requirements.txt
   
Following the requirements file, pip will install `Django <http://djangoproject.com>`_ and `Django command extensions <http://code.google.com/p/django-command-extensions/>`_.

Now you should be all set for the tutorial!
