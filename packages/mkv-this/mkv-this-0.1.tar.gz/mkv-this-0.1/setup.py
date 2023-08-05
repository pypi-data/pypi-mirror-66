from setuptools import setup, find_packages

setup(name='mkv-this',
      version='0.1',
      description='markovify text in a file and output the results to a another file. user options to set number of sentences outputted, set state size, and combine an additional input file.',
      url='http://anarchive.mooo.com',
      author='martian hiatus',
      author_email='mousebot@riseup.net',
      license='GPL',
      packages=find_packages(),
      install_requires=[
          'markovify',
      ],
      zip_safe=False)
