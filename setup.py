#!/usr/bin/env python

from os.path import join, dirname, abspath

import subprocess
from setuptools import setup, find_packages, Command
from setuptools.command.sdist import sdist


__AUTHOR__ = 'Adelina Diacu, Bogdan Virtosu'
__AUTHOR_EMAIL__ = 'virtosu.bogdan@gmail.com'
__README_PATH__ = join(abspath(dirname(__file__)), 'README.md')
__README__ = open(__README_PATH__).read()


SASS_DIRECTORIES = [
    "cmsplugin_profile/static/admin",
    "cmsplugin_profile/static/cmsplugin_profile",
]


def build_static_files():
    print "building static files"
    print subprocess.check_output("compass -v".split())
    for directory in SASS_DIRECTORIES:
        print subprocess.check_output("compass compile {} --force".format(directory).split())


class SdistCommand(sdist):

    def run(self):
        build_static_files()
        sdist.run(self)


class BuildStaticCommand(Command):
    description = "Builds required static files."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        build_static_files()


setup(
    name='cmsplugin-profile',
    version='0.1.0.pbs.3',
    description='CMS Plugin for profiles',
    long_description=__README__,
    author=__AUTHOR__,
    author_email=__AUTHOR_EMAIL__,
    maintainer_email=__AUTHOR_EMAIL__,
    url='https://github.com/virtosubogdan/cmsplugin-profile.git',
    packages=find_packages(),
    include_package_data=True,
    platforms=['any'],
    install_requires=[
        "django-cms >= 2.3, <2.3.6",
        "django-filer >= 0.9pbs, <0.9.1",
        "django-cms-blogger >= 0.7.0.pbs, <0.8.0",
        "django-cms-roles < 0.7.1",
    ],
    cmdclass={
        'build_static': BuildStaticCommand,
        'sdist': SdistCommand,
    },
)
