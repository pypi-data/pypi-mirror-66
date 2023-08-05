import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'ffclientTest',
  version = '0.4',
  author = 'Charlie Hodgkinson',
  author_email = 'charlotte.hodgkinson4@gmail.com',
  description = 'devlopment of python featureflag client',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/tmaslen/featureflagclient-python',
  packages = setuptools.find_packages(),
  classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache Software License", #update
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)