from setuptools import setup, find_packages

# Read requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='analog_daddy',  # Name of your package
    version='0.1',  # Start with a small number and increase it with every change you make
    packages=find_packages(exclude=['tests*']),  # This will find all the packages in your project
    url='git@github.com:siddhantladdha/analog_daddy.git',  # Your code's website, e.g., the GitHub repo
    license='AGPLv3',  # Choose a license
    author='Siddhant Laddha',  # Your name
    author_email='work@siddhantladdha.com',  # Your email
    description='This library is an attempt to make transistor sizing for Analog Design less painful.',  # Short description
    long_description=open('README.md').read(),  # Long description, typically put the contents of your README file
    long_description_content_type='text/markdown',  # If you use markdown for your README
    install_requires=required, # Add all your dependencies here. You can specify versions as well.
    classifiers=[
        # Add more classifiers if necessary. Check https://pypi.org/classifiers/ for a list of all classifiers.
    ],
)