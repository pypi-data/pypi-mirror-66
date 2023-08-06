import setuptools
import re
import os

long_description = ''
with open("README.md", "r") as fh:
    long_description = fh.read()

version = ''
with open('pastee/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1) # noqa

requirements = ['aiohttp>=3.3']
try:
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    pass

extras_require = {
    'docs': [
        'sphinxcontrib_trio==1.1.0',
    ]
}


class CleanCommand(setuptools.Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system(r"rmdir dist -force -r")
        os.system(r"rmdir egg-info -force -r")
        os.system(r"rmdir build -force -r")


setuptools.setup(
    name="pastee",
    url="https://github.com/creator1372/pastee",
    version=version,
    author="creator1372",
    description="Library for using Paste.ee's api",
    long_description=long_description,
    license='MIT',
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extras_require=extras_require,
    packages=setuptools.find_packages(),
    python_requires='>=3.5.3',
    cmdclass={
        "clean": CleanCommand
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
