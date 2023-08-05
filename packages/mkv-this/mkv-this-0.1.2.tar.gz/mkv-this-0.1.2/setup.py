from setuptools import setup, find_packages

setup(name='mkv-this',
      version='0.1.2',
      description='markovify user-provided text and output the results to a text file.',
      url='http://anarchive.mooo.com',
      author='martian hiatus',
      author_email='mousebot@riseup.net',
      license='AGPLv3',
      packages=find_packages(),
      install_requires=[
          'markovify',
      ],
      zip_safe=False)
