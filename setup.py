import re
from setuptools import setup, find_packages

file_text = open('playa/__init__.py').read()

def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval

setup(
    name='playa',
    version=grep('__version__'),
    url='https://github.com/zeekay/playa',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=['bin/playa'],
    install_requires=['spotipy'],
    license='MIT',
    description='Spotify playlist downloader',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',

        'License :: OSI Approved :: MIT License',
    ],
    keywords='commandline cli spotify music upload utility',
)
