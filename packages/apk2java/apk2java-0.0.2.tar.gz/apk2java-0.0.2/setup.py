#!/usr/bin/env python
 
from setuptools import setup, find_packages
 
setup(
    name='apk2java',
    version='0.0.2',
    packages=['apk2java'],
    author="MadSquirrel",
    author_email="benoit.forgette@ci-yow.com",
    description="Decompile APK to Java",
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    download_url="https://gitlab.com/MadSquirrels/mobile/apk2java",
    include_package_data=True,
    url='https://ci-yow.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning"
    ],
 
    entry_points = {
        'console_scripts': [
            'apk2java=apk2java:main',
            'apk2java_setup=apk2java:setup',
        ],
    },
    install_requires = [
    ],
    python_requires='>=3.5'
 
)
