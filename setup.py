from setuptools import setup, find_packages
from th_dummy import __version__ as version
import os


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def reqs(*f):
    return list(filter(None, [strip_comments(l) for l in open(
        os.path.join(os.getcwd(), *f)).readlines()]))

install_requires = reqs('requirements.txt')

setup(
    name='django_th_dummy',
    version=version,
    description='Django Trigger Happy : This handles the Facebook service',
    author='Olivier Demah',
    author_email='olivier@foxmask.info',
    url='https://github.com/foxmask/django-th-facebook',
    download_url="https://github.com/foxmask/django-th-facebook/archive/trigger-happy-facebook-"
    + version + ".zip",
    packages=find_packages(exclude=['th_facebook/local_settings']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    install_requires=install_requires,
    include_package_data=True,
)
