from setuptools import setup, find_packages

setup(
  name='errandkun',
  version='0.0.1',
  packages=['errandkun'],
  license='MIT',
  entry_points={
    'mkdocs.plugins': [
      'errandkun = errandkun.errandkun:ErrandKunPlugin',
    ]
  },
  python_requires='>=3.6.4',
  install_requires=[
    'mkdocs>=1.0.4'
  ]
)