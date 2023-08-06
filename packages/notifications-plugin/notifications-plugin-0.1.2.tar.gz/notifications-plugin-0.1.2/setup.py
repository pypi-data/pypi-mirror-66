 
import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def get_version():
    import os
    data = {}
    fname = os.path.join('notifications_plugin', '__init__.py')
    exec(compile(open(fname).read(), fname, 'exec'), data)
    return data.get('__version__')


install_requires = [
    'django>=2.2',
]

setup(
    name='notifications-plugin',
    author='Aditya Palaparthy',
    author_email='aditya94palaparthy@gmail.com',
    version=get_version(),
    include_package_data=True,
    url='https://pypi.python.org/pypi/notifications-plugin/',
    license='GNU General Public License v3.0',
    description='A django app to create simple notifications',
    long_description=README,
    install_requires=install_requires,
    packages=['notifications_plugin'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities'
    ],
    python_requires='>=3.1',
)