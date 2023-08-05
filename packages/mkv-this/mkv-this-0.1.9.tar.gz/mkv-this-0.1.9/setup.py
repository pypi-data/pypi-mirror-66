from setuptools import setup, find_packages

# read the contents of your README file as long_description:
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(name='mkv-this',
      version='0.1.9',
      description='markovify user-provided text and output the results to a text file.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='',
      author='mousebot',
      author_email='mousebot@riseup.net',
      license='AGPLv3',
      packages=find_packages(),
      scripts=["scripts/mkv-this"],
      install_requires=[
          'markovify',
          'argparse',
      ],
      zip_safe=False,
)
