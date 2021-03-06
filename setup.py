from setuptools import setup

version = '0.4.2'

setup(name='EZID',
      version=version,
      description="EZID api 2.0 library",
      author="Mark Redar",
      author_email="mark.redar@ucop.edu",
      url="https://github.com/ucldc/ezid",
      py_modules = ['EZID', 'DSC_EZID_minter'],
      scripts=['DSC_EZID_minter.py',],
      install_requires=[
          'future',
          'requests',
      ],
      classifiers = [
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Intended Audience :: End Users/Desktop",
          "Topic :: Internet",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Utilities",
      ],
      tests_require=['datacite']
      )

