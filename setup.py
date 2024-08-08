from setuptools import setup, find_packages

setup(
    name='pilot-py-hub-aggregator',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'google-generativeai'
    ],
    author='Piyush Kumar',
    author_email='piyushkumar121@gmail.com',
    description='A package for generating code using various AI models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lishu-gupta-pilot-tech/pilot-py-hub',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
