import setuptools

with open('README.rst','r') as redme:
  long=redme.read()

setuptools.setup(
  name = 'coolwait',         # How you named your package folder (MyLib)
  packages=setuptools.find_packages(),
#  packages = ['coolwait'],   # Chose the same as "name"
  version = '0.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'my first project on pypi',   # Give a short description about your library
  author = 'Noobie',                   # Type in your name
  author_email = 'adlizhafari122@gmail.com',      # Type in your E-Mail
  long_description=long,
  long_description_content_type="text/markdown",
  url="https://github.com/kang-newbie/colorwait",
  keywords = ['COOLWAIT','COLORWAIT'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
  python_requires='>=3',
)
