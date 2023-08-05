from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.0.2'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='openpy',
    version=__version__,
    description='Open files for humans',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/orenovadia/openpy',
    download_url='https://github.com/orenovadia/openpy/tarball/' + __version__,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    author='Oren Ovadia',
    install_requires=['s3fs','requests'],
    dependency_links=dependency_links,
    author_email='orenovad@gmail.com'
)
