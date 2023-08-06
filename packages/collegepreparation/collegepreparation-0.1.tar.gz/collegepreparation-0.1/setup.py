from setuptools import setup

with open("README.rst", "r") as l:
      long_description=l.read()

setup(name='collegepreparation',
      version='0.1',
      description='prepare textual data',
      long_description=long_description, 
      long_description_content_type="text/markdown",
      py_modules=['cleaning', 'merge', 'parse', 'readweb', 'topics'],  
      packages=['preparation'], 
      classifiers=[
            "Programming Language :: Python", 
            "Programming Language :: Python :: 3.6", 
            "Programming Language :: Python :: 3.7", 
            "Programming Language :: Python :: 3.8", 
            "License :: OSI Approved :: Academic Free License (AFL)"
      ],
      #url='stempro.org',
      author='training',
      author_email='admin@stempro.org',
      license='MIT', 
      zip_safe=False)