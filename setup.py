from pathlib import Path
from setuptools import setup
from setuptools import find_packages


here = Path(__file__).absolute().parent


EXTRAS = frozenset({
    'third_party',
})


def extras_require(all_extras=EXTRAS):
    """ Get map of all extra requirements
    """
    return {
        x: requirements(here / 'requirements' / 'extras' / f'{x}.txt') for x in all_extras
    }


def requirements(at_path: Path):
    with at_path.open() as f:
        rows = f.read().strip().split('\n')
        requires = []
        for row in rows:
            row = row.strip()
            if row and not (row.startswith('#') or row.startswith('http')):
                requires.append(row)
    return requires


with (here / 'README.rst').open() as f:
    README = f.read()


# Setup
# ----------------------------

setup(name='openapi-type',
      version='0.2.1',
      description='OpenAPI Type',
      long_description=README,
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Operating System :: POSIX',
      ],
      author='Maxim Avanov',
      author_email='maxim.avanov@gmail.com',
      url='https://github.com/avanov/openapi-type',
      keywords='typing json yaml openapi oas swagger schema serialization deserialization structured-data',
      packages=find_packages(exclude=['tests', 'tests.*']),
      include_package_data=True,
      zip_safe=False,
      test_suite='tests',
      tests_require=['pytest', 'coverage'],
      install_requires=requirements(here / 'requirements' / 'minimal.txt'),
      extras_require=extras_require(),
      entry_points={
          'console_scripts': [
              'openapi-type = openapi_type.cli:main'
          ],
      }
    )
