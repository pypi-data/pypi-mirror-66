from setuptools import setup

with open('README.md') as f:
    long_description = f.read()


def get_version():
    return open('version.txt', 'r').read().strip()


setup(name='newtools',
      version=get_version(),
      description='A selection of tools for easier processing of data using Pandas and AWS',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://bitbucket.org/dativa4data/newtools/',
      author='Dativa',
      author_email='hello@dativa.com',
      license='MIT',
      zip_safe=False,
      packages=['newtools',
                'newtools.aws'],
      include_package_data=True,
      setup_requires=[
          'setuptools>=41.0.1',
          'wheel>=0.33.4',
          'numpy>=1.13.3'],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.6'],
      keywords='dativa', )
