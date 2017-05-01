import codecs
import os
from setuptools import find_packages, setup


# semantic versioning
VERSION = '0.1.1'


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf8') as fh:
    long_description = fh.read()


setup(
    name='logging2',
    version=VERSION,
    description='A More Pythonic Logging System',
    long_description=long_description,
    url='https://github.com/vforgione/logging2',
    author='Vince Forgione',
    author_email='v.forgione@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='logging',
    packages=find_packages(where='.', exclude=['tests', 'docs'])
)
