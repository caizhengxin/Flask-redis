# -*- coding: utf-8 -*-
# @Author: caixin
# @Date:   2017-09-30 10:49:08
# @Last Modified by:   1249614072@qq.com
# @Last Modified time: 2017-10-09 17:12:26
"""
Flask-Redis
----------

A Flask extension for sending email messages.

Please refer to the online documentation for details.

Links
`````

* `documentation <http://packages.python.org/Flask-Redis>`_
"""
from setuptools import setup


setup(
    name='Flask-Redis',
    version='0.1.0',
    url='https://github.com/caizhengxin/flask-redis',
    license='BSD',
    author='caixin',
    author_email='1249614072@qq.com',
    maintainer='caixin',
    maintainer_email='1249614072@qq.com',
    description='Flask extension for redis',
    long_description=__doc__,
    packages=[
        'flask_redis'
    ],
    test_suite='test_redis',
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.8',
        'redis>=2.7.6',
        'msgpack-python>=0.4.8',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
