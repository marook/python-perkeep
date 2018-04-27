#
# -*- coding: utf-8 -*-
# python-perkeep 
# Copyright (C) 2018  Markus Peröbner
#
from distutils.core import setup

setup(name='perkeep',
      version='0.1.0',
      license='GPLv3',
      description='a client library for perkeep',
      author='Markus Peröbner',
      author_email='markus.peroebner@gmail.com',
      packages=[
            'perkeep',
            'perkeep.datasets',
      ],
      url='https://github.com/marook/python-perkeep',
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
      ],
      keywords='perkeep',
)
