import sys
import setuptools

from setuptools.command.test import test as TestCommand

import cowork


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox

        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


with open('README.rst') as reader:
    readme = reader.read()

setuptools.setup(
    name='cowork',
    version=cowork.__version__,
    description='Cowork',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author='Grant Jenks',
    author_email='contact@grantjenks.com',
    url='http://www.grantjenks.com/docs/cowork/',
    license='Apache 2.0',
    packages=['cowork'],
    include_package_data=True,
    tests_require=['tox'],
    cmdclass={'test': Tox},
    install_requires=[],
    project_urls={
        'Documentation': 'http://www.grantjenks.com/docs/cowork/',
        'Funding': 'http://gum.co/cowork',
        'Source': 'https://github.com/grantjenks/jupyter-cowork',
        'Tracker': 'https://github.com/grantjenks/jupyter-cowork/issues',
    },
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
)
