# -*- coding: utf-8 -*-

import os
from distutils.command.build import build

from django.core import management
from setuptools import setup, find_packages


try:
    with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = ''


class CustomBuild(build):
    def run(self):
        management.call_command('compilemessages', verbosity=1)
        build.run(self)


cmdclass = {
    'build': CustomBuild
}


setup(
    name='pretix-public-registrations',
    version='1.4.0',
    description='This plugin will give the option to attendees of an event to mark their registration as public. Public registrations will be shown along their answers to questions marked as public by the organizers on a world-readable page.',
    long_description=long_description,
    keywords="pretix public registrations",
    url="https://gitlab.fachschaften.org/kif/pretix-public-registrations",
    project_urls={
        "Bug Tracker": 'https://gitlab.fachschaften.org/kif/pretix-public-registrations/issues',
        "Source Code": 'https://gitlab.fachschaften.org/kif/pretix-public-registrations/tree/master',
    },
    author='Felix Schäfer, Dominik Weitz',
    author_email='admin@kif.rocks',
    license='MIT License',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    install_requires=['django-gravatar2'],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretix.plugin]
pretix_public_registrations=pretix_public_registrations:PretixPluginMeta
""",
)
