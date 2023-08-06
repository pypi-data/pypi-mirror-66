from setuptools import setup, find_packages

setup(
    name='tansa',
    version='0.0.1',
    description='JSON extractor from file path',
    long_description=open('readme.md').read(),
    long_description_content_type="text/markdown",
    author='Takashi Kato',
    author_email='taka@m.atelierpal.space',
    url='https://github.com/k0a8t1o6/tansa',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['tansa = tansa.app:main']
    }
)