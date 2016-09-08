# from distutils.core import setup
from setuptools import setup
import os

from fix import __version__

setup(
    name="fix-jolla-desktop",
    packages=["docpie"],
    package_data={
        '': [
            'README.rst',
            'LICENSE',
            '*.desktop'
        ],
    },
    version=__version__,
    author="TylerTemp",
    author_email="tylertempdev@gmail.com",
    url="https://github.com/TylerTemp/fix-jolla-desktop",
    download_url="https://github.com/TylerTemp/fix-jolla-desktop/archive/master.zip",
    license='MIT',
    description=("Fix jolla, Sailfish OS android app icon"),
    keywords='jolla sailfish',
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    entry_points={
        'console_scripts': [
            'fix = fix:main'
        ]
    }
    platforms='any',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Operating System :: Other OS',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        ],
)
