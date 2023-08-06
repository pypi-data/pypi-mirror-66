import os

from setuptools import find_packages, setup

from hosting_benchmark.version import __version__


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


with open(os.path.join(BASE_DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

extra_files = package_files(
    os.path.join(BASE_DIR, 'hosting_benchmark', 'server')
)

required_packages = [
    'click',
    'requests',
    'terminaltables',
]

extras_require = {
    "dev": ["ipython", "twine"],
    "test": ["mock", "munch", "pytest", "pytest-mock < 3.0"],
}

setup(
    name="hosting-benchmark",
    version=__version__,
    description="PHP Web-hosting benchmark",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Jakub Szafrański",
    author_email="kontakt@samu.pl",
    url="https://github.com/samupl/hosting-benchmark",
    packages=find_packages(),
    test_suite="tests",
    install_requires=required_packages,
    extras_require=extras_require,
    tests_require=extras_require["test"],
    entry_points={
        "console_scripts": [
            "hosting-benchmark = hosting_benchmark.benchmark:cli",
        ]
    },
    package_data={'': extra_files}
)
