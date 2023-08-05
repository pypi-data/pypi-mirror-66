import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'ffcharlietest',
  version = '0.4',
  author = 'Tom Maslen',
  author_email = 'tom_maslen@hotmail.com',
  description = 'Service agnostic featureflag client',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/tmaslen/featureflagclient-python',
  keywords = ['feature flag', 'feature toggle'],
  packages = setuptools.find_packages(),
  classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License", #update
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)