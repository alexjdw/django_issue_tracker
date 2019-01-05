# Sticky Ickies: A Django Issue Tracker

Welcome to my demo project: a handmade, Django-based, responsive, full-CRUD issue tracker using Django, Django Rest Framework, and SQLite.

Every element of this page is hand-coded by me, and I purposefully avoided using the familiar Foundation and Bootstrap or using a predesigned website layout. I now understand the consequences of my actions and am willing to apologize in person to your eyes if needed. I am a reformed man who will let the professional designers do their job in the future. Please see the disclaimer section below for more details.

## Getting Started

Ensure Python 3.6 is installed
Clone the Repo
Navigate to the root directory.
Set up your virtual environment with Python 3.6 (something like: virtualenv --python=/opt/python-3.6/bin/python .venv)
**Note: Django 1.11 currently does not play well with Python 3.7. Please ensure to use Python 3.6!**
Activate your virtual environment (usually: source .venv/bin/activate)
Run the following commands:

```
pip install -r requirements.txt
cd issue_tracker
./manage.py makemigrations
./manage.py migrate
./manage.py shell
```

You should see the dependencies install, and django should make the initial database migrations. After running the shell command, a shell will open. Let's make an administrator with the following commands in the shell:

```
>> from apps.users.models import User
>> u = User.objects.create(username='someemail@email.com', email='someemail@email.com', password='somepassword')
>> u.permissions.adminpage = True
>> u.save()
>> exit()
```

This will create a new user and bypass the registration key. Feel free to sub in your email and password as the information should be encrypted and this app does not collect or send your data anywhere for any reason.

After you exit(), the shell will close and you'll be back at your normal prompt. From there:

```
./manage.py runserver
```

This will start the server. Visit localhost:8000 and log in with your new username and password to get started.

# Disclaimer

This is a demo project at this time! You *will* run into many issues. At the time of this readme update, there are several linked pages that simply aren't implemented at all. However, I hope you'll find that the app is complete and usable as an issue tracker as of this moment. Please let me know if anything on the Open Issues, My Issues, New, /api, or /super routes seems to be crashing.

In addition, you'll notice that it's a bit, ahem, *ugly*. I'm creating this project completely from scratch! I'm not a designer, so icons are largely pilfered from the wonderful folks at Font Awesome, fonts are from Google Fonts, and images are either made by me or pilfered from a copyright-free search on the web. Colors were selected from an online color scheme generator. I can't say I am strong with visual design, and the lack of a framework makes updating the style and color scheme and such quite time consuming, so until functionality is complete, I'm holding off on tinkering with the minor visuals.

However, I can proudly say that every element of this website was hand-coded by me using a minimum of templated code. This project single-handedly made me rethink how my HTML, SASS, and JavaScript code should be organized. I'm still a ways away from my desired level of DRYness!

# General Usage

This is a demo project! Here's a quick tour of the working features:

login and registration:
localhost:8000 (while logged out)

api:
localhost:8000/api
A clickable API using Django REST Framework, which is a wonderful tool that made this very easy. The project itself uses its own API in several places.
To see raw JSON, add ?format=json to the end of any API URL.

post-it issue tracker:
localhost:8000/issues
- After logging in, you'll be dropped off here. Click "New" on the NavBar and add some sample issues.
- Once you have a few issues made, head back to the Open Issues page to see the postits.
- Postits are clickable!

basic admin page:
localhost:8000/super
- Make sure to use the above method to create a super user.
- Make sure to create a few issues first using the "New" tab.
- To get the full experience, create a few users.
- Click on table rows and buttons to make edits. Clicked "active" table rows will display more options.
- Clicking buttons or specific table elements will allow you to add/remove users on an issue, change the issue owner, and update the priority in real time.

search:
Search is available on /super and /issues. It suggests existing categories to search for. These are populated dynamically with AJAX based on the issues you've added.

## Deployment

It's possible to go live with this project as is, and I have tested recent builds on Amazon EC2 with Gunicorn and Nginx as my service manager and web endpoint respectively. However, this build is not production-ready. Please let me know before you deploy anything in the public space.

## Technologies

* Django 1.11.7 (https://www.djangoproject.com/)
* Django REST Framework (https://www.django-rest-framework.org/)
* jQuery & jQuery UI (https://jquery.com/)
* SASS (https://sass-lang.com/)

## Learning Moments for Me

* CSS Grids
* Editable fields using AJAX
* Modal pop-up forms
* Extending Django User models
* Proper use of SASS
* JQuery UI and Styling for JQuery UI
* Proper project layout in Django
* APIs!

## Contributing

I'm using this as a resume project, so please, no pull requests at this time. I'd like to maintain ownership of the code. Once complete, I will open up pull requests for bugs and new features. Please let me know if you plan to use this project. I take no liability for your use as this project is not complete at this time.

## Authors

* **Alex Weavers** - *Initial work* - [AWildTechno](https://github.com/awildtechno)
* **Tina Su** - *Custom Artwork*

## License
If you'd like to use this for yourself or your team, please let me know first. Feel free to clone the repo and play around!
