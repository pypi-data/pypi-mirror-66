import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


version = {}
with open("irekua_rest_api/version.py") as fp:
    exec(fp.read(), version)


setup(
    name='irekua-rest-api',
    version=version['__version__'],
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='REST API for Irekua access',
    long_description=README,
    url='https://github.com/CONABIO-audio/irekua-rest-api',
    author='CONABIO, Gustavo Everardo Robredo Esquivelzeta, Santiago Martínez Balvanera',
    author_email='erobredo@conabio.gob.mx, smartinez@conabio.gob.mx',
    install_requires=[
        'irekua_database',
        'irekua_filters',
        'irekua_permissions',
        'djangorestframework',
        'markdown',
        'django-filter',
        'coreapi',
        'pyyaml',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
