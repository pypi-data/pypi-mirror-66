import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="py-lambda-base", # Replace with your own username
  version="0.0.6-dev24",
  author="Michael Madison",
  author_email="cadetstar@hotmail.com",
  description="Pseudo-application for AWS Lambda",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/pypa/sampleproject",
  packages=setuptools.find_packages(),
  install_requires=[
    'deepmerge==0.1.0',
    'dpath==2.0.1',
    'json-api-doc==0.11.0'
  ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)
