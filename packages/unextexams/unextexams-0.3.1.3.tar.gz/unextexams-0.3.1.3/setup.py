import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setuptools.setup(
  name = 'unextexams',
  install_requires=REQUIREMENTS,
  version = '0.3.1.3',
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
    ],
    python_requires='>=3.6',

)
