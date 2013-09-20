from setuptools import find_packages
from setuptools import setup

setup(name='newsletters',
      version='0.1',
      description='ixxy url field',
      author='Andy Baker',
      author_email='andy@andybak.net',
      packages=find_packages(),
      package_data={
          'newsletters': [
            'static/admin/*',
          ]
      },
      include_package_data=True,
)
