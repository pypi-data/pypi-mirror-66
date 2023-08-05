#! /usr/bin/env python
from setuptools import setup

VERSION = '1.9.2'

def main():
    setup(name='par2deep',
          version=VERSION,
          description="Produce, verify and repair par2 files recursively. ",
          long_description=open('README.md').read(),
          long_description_content_type="text/markdown",
          classifiers=[
              'Development Status :: 5 - Production/Stable',
              'Environment :: Console',
              'Environment :: MacOS X',
              'Environment :: Win32 (MS Windows)',
              'Environment :: X11 Applications',
              'Programming Language :: Python :: 3',
              'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
              'Topic :: Utilities',
              'Operating System :: OS Independent'
          ],
          keywords='par2 file integrity',
          author='Brent Huisman',
          author_email='mail@brenthuisman.net',
          url='https://github.com/brenthuisman/par2deep',
          license='LGPL',
          include_package_data=True,
          zip_safe=False,
          install_requires=['tqdm','configargparse','Send2Trash','PyQt5'],
          packages=['par2deep'],
          entry_points={
              "console_scripts": ['par2deep = par2deep.gui_qt:main', 'par2deep-tk = par2deep.gui_tk:main', 'par2deep-cli = par2deep.cli:main'],
          }
          )

if __name__ == '__main__':
    main()
