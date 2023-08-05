from setuptools import setup, find_packages

setup(
  name='errandkun',
  version='0.0.6',
  packages=find_packages(),
  license='MIT',
  entry_points={
    'mkdocs.plugins': [
      'errandkun = errandkun.errandkun:ErrandKunPlugin',
    ]
  },
  python_requires='>=3.6.4',
  install_requires=[
    'mkdocs>=1.0.4',
    'requests'
  ],
  include_package_data = True
)