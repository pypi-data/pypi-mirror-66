#!/usr/bin/env python3

import os

import setuptools


if __name__ == '__main__':
    readme_filename = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_filename, encoding='utf-8') as readme_file:
        readme = readme_file.read()
    setuptools.setup(
        name='django-cms-qe',
        version='1.4.3',
        packages=setuptools.find_packages(exclude=[
            '*.tests',
            '*.tests.*',
            'tests.*',
            'tests',
            'test_utils.*',
            'test_utils',
            '*.migrations',
            '*.migrations.*',
        ]),
        include_package_data=True,
        description=(
            'Django CMS Quick & Easy provides all important modules to run new page without'
            'a lot of coding. Aims to do it very easily and securely.'
        ),
        long_description=readme,
        url='https://websites.pages.labs.nic.cz/django-cms-qe',
        author='CZ.NIC, z.s.p.o.',
        author_email='kontakt@nic.cz',
        license='BSD License',

        # All versions are fixed just for case. Once in while try to check for new versions.
        install_requires=[
            'aldryn-boilerplates==0.7.7',
            'aldryn-bootstrap3==1.3.0',
            'aldryn-forms==3.0.3',
            'argon2_cffi==16.3.0',
            'cmsplugin-filer==1.1.3',
            'Django>=1.11.0,<2.0',
            'django-axes==2.3.3',
            'django-bootstrap-form==3.3',
            'django-cms==3.5.2',
            'django-constance[database]==2.0.0',
            'django-csp==3.3',
            'django-filer==1.3.2',
            'django-import-export==0.5.1',
            'tablib==0.14.0',  # Used by django-import-export
            'django-jsonfield==1.0.1',
            'django-mail-queue==3.1.4',
            'django-settings==1.3.12',
            'djangocms-googlemap==1.1.1',
            'djangocms-text-ckeditor==3.5.1',
            'djangocms-attributes-field>=0.1.1',  # Used by cms-qe-video
            'djangocms-inline-comment==0.0.2',
            'easy-thumbnails==2.5.0',  # Used by Django Filer
            'mailchimp3==2.0.15',
            'python-memcached==1.59',
            'pytz',
        ],
        # Do not use test_require or build_require, because then it's not installed and is
        # able to be used only by setup.py util. We want to use it manually.
        # Actually it could be all in dev-requirements.txt but it's good to have it here
        # next to run dependencies and have it separated by purposes.
        extras_require={
            'dev': [
                'django-debug-toolbar==1.8',
                'django_extensions==1.9.6',
            ],
            'test': [
                'mypy==0.620',
                'pylint==1.9.2',
                'pylint-django==0.11.1',
                'pytest==3.6.3',
                'pytest-data==0.4',
                'pytest-django==3.3.2',
                'pytest-env==0.6.2',
                'pytest-pythonpath==0.7.1',
                'pytest-sugar==0.9.1',
                'pytest-watch==4.2.0',
                'pyvirtualdisplay==0.2.1',
                'webdriverwrapper==2.5.0',
            ],
            'build': [
                'Sphinx==1.6.5',
            ],
            'psql': [
                'psycopg2==2.7.3',
            ],
            'mysql': [
                'mysqlclient==1.3.14',
            ],
        },

        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Natural Language :: English',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Libraries :: Application Frameworks',
            'Framework :: Django',
            'Framework :: Django :: 1.10',
            'Framework :: Django :: 1.11',
        ],
        keywords=['django', 'cms'],
    )
