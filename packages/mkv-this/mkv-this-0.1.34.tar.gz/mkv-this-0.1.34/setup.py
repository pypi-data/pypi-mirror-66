from setuptools import setup, find_packages

# read the contents of your README file as long_description:
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(name='mkv-this',
      version='0.1.34',
      description='cli wrapper for markovify: take a text file or URL, markovify, save the results.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://git.disroot.org/mousebot/mkv-this',
      author='mousebot',
      author_email='martianhiatus@riseup.net',
      license='AGPLv3',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'mkv-this = mkv_this.mkv_this:main',
              'mkv-this-dir = mkv_this.mkv_this_dir:main'
              ]
          },
      install_requires=[
          'markovify',
          'argparse',
          'html2text',
      ],
      zip_safe=False,
)
