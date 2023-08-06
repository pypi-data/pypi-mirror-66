import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
print(long_description)
setuptools.setup(
  name = 'findimport',         # How you named your package folder (MyLib)
  packages = ['findimport'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  setup_requires=['wheel'],
  long_description=long_description,
  long_description_content_type="text/markdown",
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This is a simple library to find the recursive import link of source code',   # Give a short description about your library
  author = 'VigneshAmudha',                   # Type in your name
  author_email = 'vigneshgig@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/vigneshgig/Python-Find-imported-Module',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/vigneshgig/Python-Find-imported-Module/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Module Finder', 'Import Finder', 'Module Tracker','Import Tracker'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',      #Specify which pyhton versions that you want to support

  ],
)
