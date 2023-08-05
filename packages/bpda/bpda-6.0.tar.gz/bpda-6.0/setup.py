import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(name='bpda',
      version='6.0',
      description='BingPanDevApi.py: Make Old Bing Pics Can Access',
      author='Jack',
      author_email='admin@rdpstudo.top',
      maintainer='Jack',
      maintainer_email='admin@rdpstudo.top',
      url=' http://rdpstudio.top',
      packages=setuptools.find_packages(),
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="Public domain",
      install_requires=['requests'],
      platforms=["any"],
     )
