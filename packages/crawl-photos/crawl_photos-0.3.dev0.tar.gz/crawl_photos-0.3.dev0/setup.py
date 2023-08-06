# -*- coding: utf-8 -*-

from setuptools import setup
import crawl_photos

setup(
    name='crawl_photos',
    version=crawl_photos.__version__,
    author=crawl_photos.__author__,
    author_email='1830mm@sina.com',
    description='a test',
    license='MIT',
    url='https://github.com/mcwt/crawl_photos',
    py_modules=['crawl_photos'],
    scripts=['crawl_photos.py'],
    entry_points={
        'console_scripts': [
            'crawl_photos = crawl_photos:main'
        ]
    }

)
