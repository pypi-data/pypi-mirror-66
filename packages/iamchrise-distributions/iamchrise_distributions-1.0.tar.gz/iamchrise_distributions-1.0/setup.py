from setuptools import setup

with open("iamchrise_distributions/README.md", "r") as fh:
    long_description = fh.read()

setup(name='iamchrise_distributions',
      version='1.0',
      description='Gaussian and Binomial distributions',
      packages=['iamchrise_distributions'],
      author = 'Christian Emiyah',
      author_email = 'christian.emiyah@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url = 'https://github.com/emichris/Distribution-Pakage-Files',
      classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      
      zip_safe=False)
