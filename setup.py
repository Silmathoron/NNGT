#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
        name='nngt',
        version = '0.5',
        description = 'Package to study growth and activity of neural networks',
        package_dir={'': '.'},
        packages = find_packages('.'),
        
        # Include the non python files:
        package_data = { '': ['*.txt', '*.rst', '*.md', '*.default'] },
        
        # Requirements
        install_requires = [ 'numpy', 'scipy>=0.11', 'matplotlib' ],
        extras_require = {
            'PySide': ['PySide'],
            'PDF':  ["ReportLab>=1.2", "RXP"],
            'reST': ["docutils>=0.3"],
            'nx': ['networkx'],
            'ig': ['python-igraph']
        },
        entry_points = {
            #@todo
            #~ 'console_scripts': [
                #~ 'rst2pdf = nngt.tools.pdfgen [PDF]',
                #~ 'rst2html = nngt.tools.htmlgen'
            #~ ],
            'gui_scripts': [ 'netgen = nngt.gui.main.__main__:main [PySide]' ]
        },
        
        # Metadata
        url = 'https://github.com/Silmathoron/NNGT',
        author = 'Tanguy Fardet',
        author_email = 'tanguy.fardet@univ-paris-diderot.fr',
        license = 'GNU',
        keywords = 'neural network graph simulation NEST topology growth'
)
