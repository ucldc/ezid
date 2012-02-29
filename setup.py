from distutils.core import setup

version = '0.1'

setup(name='EZID',
      version=version,
      description="EZID api 2.0 library",
      author="Mark Redar",
      author_email="mark.redar@ucop.edu",
      url="https://bitbucket.org/mredar/ezid",
      py_modules = ['EZID'],
      scripts=['DSC_EZID_minter.py',],
      classifiers = [
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Intended Audience :: End Users/Desktop",
          "Topic :: Internet",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Utilities",
      ],
      )

