from setuptools import setup, find_packages

description = 'New testament greek app for django.'
long_desc = open('README.rst').read()

setup(
    name='django-greekapp',
    version='0.0.3',
    url='https://github.com/honza/greekapp',
    install_requires=['django', 'redis'],
    description=description,
    long_description=long_desc,
    author='Honza Pokorny',
    author_email='me@honza.ca',
    maintainer='Honza Pokorny',
    maintainer_email='me@honza.ca',
    packages=find_packages(),
    zip_safe=False,
    package_data={
        'greekapp': [
            'templates/greekapp/*.html',
            'static/*',
            'management/commands/nt.db'
        ]
    }
)
