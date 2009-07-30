from setuptools import setup, find_packages

version = '0.4.3'

setup(name='deam',
      version=version,
      description="django external apps manager",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='django apps custom-command',
      author='Kenny Belizky & Martin Saizar',
      author_email='kenny@belitzky.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
