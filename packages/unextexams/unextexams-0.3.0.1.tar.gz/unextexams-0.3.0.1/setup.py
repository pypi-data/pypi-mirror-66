import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'unextexams',
  version = '0.3.0.1',
  author = 'Isaac Zainea',
  author_email = 'isaaczainea@gmail.com',  
  description = 'paquete de examenes - Universidad Externado',
  url = 'https://github.com/MCG-Externado/unextexams', # use the URL to the github repo
  keywords = ['testing', 'exams', 'Externado'],
  packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
