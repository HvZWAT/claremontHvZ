Claremont Humans vs. Zombies Site
====================================

# Humans vs. Zombies Mailer

This is a mailer application for moderators of the 5C-wide game, Humans vs. Zombies. It allows moderators to quickly email subsets of players registered in the HvZ website. The mailer is only accessible to those with Django admin privileges (which HvZ moderators should have). 

## Architecture
### Prerequisites
Python 3,
Django 2.0,
Git

### Gems
Virtualenv,
Compass

## Installation
These are the installation instructions from the original creators of the HvZ website with a few modifications to make some parts clearer. 

### Dev machine setup

Developing for the site will require [Django](http://www.djangoproject.com/), [VirtualEnv](http://pypi.python.org/pypi/virtualenv/),
and [Compass](http://rubygems.org/gems/compass). If you are familiar with and have (or know how to
get) all of these, feel free to skip this section. When installing these, you’ll want to make sure that you are downloading Django version 2.0 and that your VirtualEnv is set up with Python3 by default. The latter can be done with the `pip3 install virtualenv` command mentioned below.

First off, install [pip](http://www.pip-installer.org/) using your favorite package manager. If you're developing on a Mac, I recommend installing/using [homebrew](http://mxcl.github.io/homebrew/) as your package manager of choice. Then `brew install python3` will install pip.

Using pip, you should have an easy time installing virtualenv:

    pip3 install virtualenv

Secondly, you'll need to install [Compass](http://rubygems.org/gems/compass). You can do this with

    sudo gem install compass

If you don't have RubyGems installed, get Compass installed using your
favorite package manager or method.

### Building the site

Note: Make sure to follow these steps in order (particularly 
creating the virtualenv before cloning your GitHub repo) to avoid
potential bugs.

Now create a root directory for your site. Mine is
`~/programming/claremonthvz.org`.

Note that I'm going to refer to `~/programming` everywhere. If your
root directory is in a different place, use your imagination and
substitute accordingly.

Now build a virtualenv in the root directory, which for me was

    virtualenv -p python3 ~/programming/claremonthvz.org

Virtualenv provides a wrapper between your machine and the site. As
long as the site only interacts with packages inside this wrapper, we
know that we can port the site over to other machines without
accidentally relying on some random laptop's quirks.

To actually *use* the virtualenv, you'll need to activate it:

    source ~/programming/claremonthvz.org/bin/activate

This command only affects your current terminal, so you'll need to
rerun it every time you want to work on the site. I highly recommend (although
this is only for your convenience and is not necessary unless you want to avoid
retyping these same commands each time you set up your virtualenv)
you add an alias to your .bashrc along the lines of

    alias hvz="cd ~/programming/claremonthvz.org && source bin/activate && cd claremontHvZ/HVZ"

Clone your forked GitHub repo (you don't have to use the command line
for this):

    git clone https://github.com/HvZWAT/claremontHvZ.git

Enter into the claremontHvZ directory

    cd claremontHvZ

Now complete the build with

    python3 setup.py

It is likely that after running this command, you will receive an error: `ModuleNotFoundError: No module named <module_name>`. If you receive this error, run the command `pip3 install <module_name>` where <module_name> will be the name of some module such as “django” or “markdown”. After installing the given module with the aforementioned command, rerun the above command `python setup.py` to complete the build. If necessary, repeat these steps to import any missing modules until the build successfully completes.

If prompted to create a superuser, enter a username, email, 
and password of your choice. This will be used to log into the 
HvZ website once you start running a development version of
the server. This user account will have admin privileges as well. 

If you have not been prompted to create a superuser during this 
process, enter the following command and follow the prompts to 
enter a username, email, and password of your choice.

    python3 manage.py createsuperuser

If all went well, that should be it! 

### Running a development version of the server

To run a development version of the server:

    python3 manage.py runserver

You can then access the site by directing your browser to `localhost:8000`.

### Running unit tests

To run our unit tests:

    python3 manage.py test HVZ

These tests will check registration, feeding, and permission scenarios.

## Functionality
### W.A.T.:
* Mailer button in navigation bar
* Mailer form interface 
* Filter by player type
* Multiple school selection filter, the default is all schools are selected
* Single file attachments
* BCC recipient list
* Rotating sender address to get away with the Google's email limit

### Red Bunnies:
* Filter by each college
* Failure page
* Print out player list

## Known Problems
To check if you have created your virtual environment correctly for python, use `which python3` to check your python path
If python’s path is the actual directory of your virtual environment, then it is at the right place.
If not, then we suggest you to recreate a virtual environment again

Use “pip3 install” to resolve missing modules (django, markdown, etc…).
If you ever get a “no module named ‘root’” error or “returned non-zero exit status 1” developers don’t know how to resolve that yet. Best of luck to you.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D


