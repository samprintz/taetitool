from setuptools import setup, find_packages

setup(name='taetitool',
      version='0.2.0',
      packages=find_packages(),
      zip_safe=False,
      entry_points={
          'console_scripts': ['taetitool=taetitool.__main__:main'],
      }
      )
