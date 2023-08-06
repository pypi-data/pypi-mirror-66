=========
django-image-wrapper
=========

django-image-wrapper is a library which helps you in rendering placeholder or actual images 

in your Djangp Template without much of hassle 

.. image:: https://coveralls.io/repos/github/zostera/django-fa/badge.svg?branch=master
    :target: https://coveralls.io/github/zostera/django-fa?branch=master

.. image:: https://travis-ci.org/zostera/django-fa.svg?branch=master
    :target: https://travis-ci.org/zostera/django-fa


Installation
------------

1. Install using pip:

   ``pip install django-picsum``


2. Add to INSTALLED_APPS in your ``settings.py``:

   ``'image_wrapper',``




Example template
----------------

   .. code:: Django

    {% load image_wrapper %}
    
    # Loads the tag

    {% pic_rand height=300 width=400 %}

    # A random image with a height of 300 and width of 400

    {% pic_rand width=300 %}

    # A random image with a height and width of 300 (300* 300 ) image 
    
     {% pix_image q="hi" min_width=100 %}

    # A image from Pixabay 

    {% pic_rand width=500  class="avatar__img" %} 

    # You can pass class and id to the image to control it in your CSS it is completely optional

     To  use images from Pixabay declare your API Key in settings.py INSTALLED_APPS
     
     PIXABAY_KEY =<YOUR KEY>


Requirements
------------

Django >= 2.0 and a matching Python version


Bugs and requests
-----------------

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

 https://github.com/VarthanV/django-picsum/issues


License
-------

You can use this under the MIT License. See `LICENSE <LICENSE>`_ file for details.


Author
------

Developed and maintained by `Vishnu Varthan Rao  <https://zostera.nl/>`_.
