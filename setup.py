from setuptools import find_packages
from setuptools import setup

setup(name='select-url-field',
      version='0.1',
      description='select url field',
      author='Andy Baker',
      author_email='andy@andybak.net',
      packages=find_packages(),
      package_data={
          'select_url_field': [
            'static/admin/*',
          ]
      },
      include_package_data=True,
)
