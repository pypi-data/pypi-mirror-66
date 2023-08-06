import setuptools

setuptools.setup(
     name='abtpackage',
     version='1.0.1',
     author="Ashta Bhuja Tripathi",
     author_email="tripathiab13@gmail.com",
     packages=['abtpackage', 'tests'],
     description="abtpackage Public Interface",
     long_description=open('README.txt').read(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
