from setuptools import setup

from cheesebread import __version__ as VERSION

with open('README.rst') as fobj:
    long_description = fobj.read()

setup(
    author='g4brielvs',
    author_email='g4brielvs@g4brievs.me',
    name='cheesebread',
    version=VERSION,
    description='cheesebread: a toolbox for data science',
    long_description=long_description,
    keywords='toolbox, data science',
    license='GPLv3+',
    url='https://github.com/g4brielvs/cheesebread',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
    python_requires='>=3.7',
    packages=[
        'cheesebread',
        'cheesebread.datasets',
        'cheesebread.helpers',
        'cheesebread.wrappers',
    ],
    install_requires=[
        'aiofiles',
        'aiohttp',
        'boto3',
        'pandas>=0.24',
        'requests',
        'riprova',
        'tqdm',
    ],
    zip_safe=False,
)

       
