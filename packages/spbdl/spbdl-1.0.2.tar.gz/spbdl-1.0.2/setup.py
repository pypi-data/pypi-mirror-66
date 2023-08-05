from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
  name = 'spbdl',
  packages = ['spbdl'],
  version = '1.0.2', 
  license='MIT',
  description = 'Download images from shitpostbot database',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Boidushya Bhattacharya',
  author_email = 'boidushyabhattacharya@gmail.com', 
  url = 'https://github.com/Boidushya/spbdl',
  download_url = 'https://github.com/Boidushya/spbdl/archive/v_01.tar.gz', 
  keywords = ['shitpostbot', 'spb', 'spbdl'], 
  install_requires=[
          'requests',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)