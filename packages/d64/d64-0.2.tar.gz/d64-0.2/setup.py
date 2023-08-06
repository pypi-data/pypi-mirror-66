from setuptools import setup

setup(name='d64',
      description='Read and write Commodore disk images',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      packages=['d64'],
      author='Simon Rowe',
      author_email='srowe@mose.org.uk',
      url='https://eden.mose.org.uk/gitweb/?p=python-d64.git',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
      )
