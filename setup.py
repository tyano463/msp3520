from setuptools import setup, Extension

setup(
    name='msp3520',
    version='0.1',
    description='A library for displaying text on the MSP3520 display.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['msp3520'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)

