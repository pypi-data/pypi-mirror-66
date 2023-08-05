"""A setup script for the package to distribute it to PyPi."""
from setuptools import setup


def README():
    """Return the contents of the README file for this project."""
    with open('README.md') as README_file:
        return README_file.read()


setup(
    name='bad-setuptools-git-version',
    url='https://github.com/st7105/bad-setuptools-git-version',
    author='st7105',
    author_email='st7105@gmail.com',
    description='Automatically set package version using git tags.',
    version="1.0.8",
    long_description=README(),
    long_description_content_type='text/markdown',
    keywords='setuptools git version-control',
    license='MIT',
    classifiers=[
        'Framework :: Setuptools Plugin',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
    ],
    py_modules=['bad_setuptools_git_version'],
    install_requires=[
        'setuptools >= 8.0',
    ],
    entry_points={
        'distutils.setup_keywords': [
            'version_config = bad_setuptools_git_version:validate_version_config'
        ],
        'console_scripts': [
            'bad-setuptools-git-version = bad_setuptools_git_version:get_version'
        ]
    }
)
