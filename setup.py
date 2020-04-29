from setuptools import setup, find_packages
import sys

version = '1.9.0'

f = open('README.md')
long_description = f.read()
f.close()

requires = ['six']
if sys.version_info[0] == 2:
    if sys.version_info[1] in (4, 5):
        requires.append('simplejson < 2.0.10')

setup(name='quantumrand',
      version=version,
      description="A Python interface to the ANU Quantum Random Numbers Server; Maintained fork of quantumrandom",
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
      ],
      keywords='quantum random number generator',
      author='Jason Carpenter',
      author_email='brad@identex.co',
      url='http://github.com/identex/quantumrand',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=requires,
      test_suite='nose.collector',
      tests_require=['nose', 'mock'],
      entry_points="""
        [console_scripts]
        qrand = quantumrand.cmd:main
        qrand-dev = quantumrand.dev:main
      """,
      )
