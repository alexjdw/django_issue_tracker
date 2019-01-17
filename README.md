# Sticky Notes: A Django Issue Tracker

Welcome to my demo project: a handmade, responsive, full-CRUD issue tracker using Django, Django Rest Framework, and SQLite.

Every element of this project is hand-coded by me, and I purposefully avoided using the familiar Foundation and Bootstrap frameworks or using a predesigned website layout. I now understand the consequences of my actions. I am a reformed man who will let the professional designers do their job in the future. Please see the disclaimer section below for more details.

The purpose of this project is to demonstrate a CRUD application that implements the most common features used on the web today. I decided on Django for a server framework and worked in a thorough API, custom SCSS, and responsive design elements. AJAX with jQuery is used for the majority of dynamic content, and the animations and user interface are handled with mostly custom code and a smattering of jQuery. It worked so well for me that I started tracking its own issues and planned features!

## Getting Started

```
Ensure Python 3.6 is installed.
Clone the Repo.
Navigate to the root directory.
Set up your virtual environment with Python 3.6:
virtualenv --python=/opt/python-3.6/bin/python .venv
**Note: Django 1.11 currently does not play well with Python 3.7. Please ensure to use Python 3.6!**
Activate your virtual environment (usually: source .venv/bin/activate)
Run the following commands:

pip install -r requirements.txt
cd issue_tracker
./manage.py makemigrations
./manage.py migrate
./manage.py shell
```

You should see the dependencies install, and Django should make the initial database migrations. After running the shell command, a shell will open. Let's make an administrator with the following commands in the shell:

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

This is a demo project at this time! You *will* run into many issues. There may be several linked pages that simply aren't implemented at all. However, I hope you'll find that the app is complete and usable as an issue tracker as of this moment. Please let me know if you find a terminal bug.

In addition, you'll notice that it's a bit, ahem, *ugly*. I'm not a designer, so icons are largely pilfered from the wonderful folks at Font Awesome, fonts are from Google Fonts, and other images are either made by me or taken from a copyright-free search on the web. Colors were selected from an online color scheme generator. Until functionality is complete, I'm holding off on tinkering with the visuals.

However, I can proudly say that every element of this website was styled and coded by me using a minimum of templated code. This project single-handedly made me rethink how my HTML, SASS, and JavaScript code should be organized. I'm still a ways away from my desired level of DRYness!

# General Usage

This is a demo project not suited for production use. Here's a quick tour of the working features:

### login and registration:
localhost:8000 (while logged out)

### api:
localhost:8000/api
- A clickable API using Django REST Framework, which is a wonderful tool that made this very easy. The project itself uses its own API in several places.
- To see raw JSON, add ?format=json to the end of any API URL.

### post-it issue tracker:
localhost:8000/issues
- After logging in, you'll be dropped off here. Click "New" on the NavBar and add some sample issues using the form.
- Once you have a few issues made, head back to the Open Issues page to see the postits.
- Postits are clickable on most pages.

### basic admin page:
localhost:8000/super
- Make sure to use the above method to create a super user.
- Make sure to create a few issues first using the "New" link.
- To get the full experience, create a few more users by logging out and using the registration form. (Registration keys are disabled for now.)
- Click on table rows and buttons to make edits. Clicked "active" table rows will display more options.
- Clicking buttons or specific table elements will allow you to add/remove users on an issue, change the issue owner, and update the priority in real time.

### search:
Search is available while logged in. It suggests existing categories to search for. These are populated dynamically with AJAX based on the issues you've added in the past.

## Deployment

It's possible to go live with this project as is, and I have tested recent builds on Amazon EC2 with Gunicorn and Nginx as my service manager and gateway respectively. However, this build is not production-ready. Please let me know before you deploy anything in the public space.

## Technologies

* [Django 1.11](https://www.djangoproject.com/)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [jQuery & jQuery UI](https://jquery.com/)
* [SASS](https://sass-lang.com/)

## Learning Moments for Me

* CSS Grids
* Editable fields using AJAX
* Modal pop-up forms
* Extending Django User models
* Proper use of SASS
* JQuery UI and Styling for JQuery UI
* Proper project layout in Django
* APIs!
* Search!

## Contributing

I'm using this as a resume project, but feel free to submit a pull request for anything you like.

## More About Me

Thanks again for viewing this. I've been developing simple programs in C++, Basic, and other languages since I was a teenager, so I suppose you could say I have about 20 years of coding experience. Life took me on other paths, and I worked as a content writer for some time. I'm currently attending a 3 month, 80-hour-a-week bootcamp program in San Jose to find out what professional software development really entails and learn the latest technologies. If you're seeking a Flask, Django, Angular, React, or Spring full-stack developer, I'd love to hear from you.

## Authors

* **Alex Weavers** - *Initial work* - [AWildTechno](https://github.com/awildtechno)
* **Tina Su** - *Custom Artwork*

## License
If you'd like to use this for yourself or your team, please let me know first. Feel free to clone the repo and play around!
