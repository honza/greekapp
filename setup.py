from setuptools import setup

description = 'New testament greek app for django.'
long_desc = open('README.md').read()

setup(
    name='django-greekapp',
    version='0.0.1',
    url='https://github.com/honza/greekapp',
    install_requires=['django', 'redis'],
    description=description,
    long_description=long_desc,
    author='Honza Pokorny',
    author_email='me@honza.ca',
    maintainer='Honza Pokorny',
    maintainer_email='me@honza.ca',
    packages=['greekapp'],
    package_data={
        'greekapp': [
            'templates/greekapp/index.html',
            'static/greekapp.min.js',
            'static/greekapp.css'
        ]
    }
)
