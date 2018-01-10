# douglasdaly.git

_Django Web application for www.DouglasDaly.com_

### Description

-----

This Django project includes a CMS application and a Blog application for my website at www.DouglasDaly.com


### Installation

-----

To clone the repository code:

```bash
$ git clone https://github.com/douglasdaly/douglasdaly
```

Then setup the python requirements - inside a virtualenv:

```bash
$ pip install -r requirements.txt
``` 

Navigate to the `douglasdaly` directory and then to initialize the database:

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

And to run the development server:

```bash
$ python manage.py runserver
```

### About

-----

This website relies on [Bootstrap](www.getbootstrap.com), [Font Awesome](www.fontawesome.com), [popper.js](www.popper.js.org) and [jQuery](www.jquery.com) for web components.

The markdown for the code presented on the blog is based on the blog post at [Ignored By Dinosaurs](https://www.ignoredbydinosaurs.com/posts/275-easy-markdown-and-syntax-highlighting-django).

### License

-----

This project is licensed under the MIT license.
