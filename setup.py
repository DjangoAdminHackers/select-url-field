from setuptools import find_packages
from setuptools import setup

setup(name='ixxy-url-field',
      version='0.1',
      description='ixxy url field',
      author='Andy Baker',
      author_email='andy@andybak.net',
      packages=find_packages(),
      package_data={
          'ixxy_url_field': [
            'static/admin/*',
          ]
      },
      include_package_data=True,
)
