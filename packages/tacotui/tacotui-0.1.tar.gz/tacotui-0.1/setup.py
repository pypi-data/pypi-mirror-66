from setuptools import setup, find_packages

version = {}
with open('tacotui/version.py', 'r') as f:
    exec(f.read(), version)

setup(
    name='tacotui',
    version=version['__version__'],
    description='Terminal text coloring and simple user interface widgets.',
    long_description='Terminal text coloring and simple user interface widgets.',
    url = 'https://tacotui.readthedocs.io/',
    author='Collin J. Delker',
    author_email='developer@collindelker.com',
    python_requires='>=3.6',
    packages=find_packages(),
    package_dir={'tacotui': 'tacotui'},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        ]
    )
