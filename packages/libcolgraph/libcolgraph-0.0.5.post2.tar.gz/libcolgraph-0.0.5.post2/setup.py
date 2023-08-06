#!/usr/bin/env python3
# setup.py

import setuptools
from distutils.core import setup, Extension
from distutils.command.build import build
from setuptools.command.build_py import build_py as _build_py


class build_py(_build_py):
    def run(self):
        self.run_command('build_ext')
        return super().run()

colgraph_cpp_module = Extension('libcolgraph._libcolgraph',
                            sources=['libcolgraph/libcolgraph.i',
                                     'libcolgraph/Graph.cpp',
                                     'libcolgraph/Vertex.cpp'],
                            include_dirs = ['libcolgraph/*.h',
                                            'libcolgraph/swigsources/*'],
                            swig_opts=['-c++'],
                            extra_compile_args=['-std=gnu++11'])

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(name='libcolgraph',
      cmdclass = {'build_py': build_py},
      ext_modules=[colgraph_cpp_module],
      py_modules=['libcolgraph',
                  'libcolgraph.colgraphweb'],
      entry_points = {
        'console_scripts': ['colgraphplot = libcolgraph.__main__:plotfromfile',
                            'colgraphweb = libcolgraph.colgraphweb.__main__:main'],
      },
      packages = setuptools.find_packages(),
      include_package_data=True,
      package_data={'colgraphweb': ['*.html', '*.css', '*.js']},
      version='0.0.5.post2',
      description='this library provides support to construct graphs and their '
                  'coloring graphs. a coloring graph is a metagraph '
                  'representing all the valid colorings of a graph. each '
                  'vertex of a coloring graph represents a coloring of the '
                  'base graph.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/aalok-sathe/coloring-graphs.git',
      author='Coloring Graphs lab, Univeristy of Richmond',
      author_email='aalok.sathe@richmond.edu',
      license='LGPL-3',
      install_requires = [
            'coloredlogs>=10.0',
            'typing>=3.6.6',
            'tqdm>=4.19.4',
            'pyvis>=0.1.6.0',
            'setuptools>=38.5.1',
            'Flask>=0.12.2',
            'networkx>=2.3',
            'PySimpleGUI>=4.0.0',
            'matplotlib>=3.0',
          ],
                 #[line[:-1] 
                 #for line in open('requirements.txt', 'r').readlines()], 
      python_requires='>=3.4',
      classifiers=[
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU Lesser General Public License v3 '
                                      'or later (LGPLv3+)',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries :: Python Modules'])
