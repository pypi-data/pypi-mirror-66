from distutils.core import setup
from setuptools import setup,setuptools
import os 
with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme_file:
    readme = readme_file.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-picsum',
    version='1.1',
    url ='https://github.com/VarthanV/django-picsum.git',
    packages=setuptools.find_packages(),
    include_package_data=True,
    long_description_content_type= 'text/markdown',
    long_description=open('README.rst').read(),
    author = "Vishnu Varthan Rao",
    author_email="vishnulatha006@gmail.com",
    install_requires=[
        "Django > 2.0",
        "requests"
    ],
    license="MIT License",
    zip_safe=False,
    keywords='picsum,pixabay,django-pics,django image,django template',
     classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],

)