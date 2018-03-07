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

Then setup the python requirements and environment variables needed - inside a virtualenv:

```bash
$ make configure
``` 

#### Debug

To setup the development environment:

```bash
$ make debug_setup
```

And to run the development server:

```bash
$ make debug
```

#### Production

To setup the production environment:

```bash
$ make setup
```

And to run the production server:

```bash
$ make start
```

or to run the whole install & run process for production just call:

```bash
$ make all
```

### About

-----

This website relies on [Bootstrap](https://www.getbootstrap.com/), [Font Awesome](https://www.fontawesome.com/), [popper.js](https://www.popper.js.org/) and [jQuery](https://www.jquery.com/) for web components.

The markdown for the code presented on the blog is based on the blog post at [Ignored By Dinosaurs](https://www.ignoredbydinosaurs.com/posts/275-easy-markdown-and-syntax-highlighting-django).

The search functionality for the blog is based on the post at [Julien Phalip's blog](https://www.julienphalip.com/blog/adding-search-to-a-django-site-in-a-snap/).

### License

-----

This project is licensed under the MIT license.
