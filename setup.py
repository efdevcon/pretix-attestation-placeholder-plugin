import os
from distutils.command.build import build

from setuptools import find_packages, setup


try:
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''


class CustomBuild(build):
    def run(self):
        from django.core import management
        management.call_command('compilemessages', verbosity=1)
        build.run(self)


cmdclass = {
    'build': CustomBuild
}

extras_require = {
    'test': [
        'pytest>=5.1,<6',
        'pytest-django>=3.5,<4',
    ],
    'lint': [
        'flake8>=3.7,<4',
        'mypy==0.720',
    ],
    'dev': [
        'tox>=3.14.5,<4',
    ],
}

extras_require['dev'] = (
    extras_require['dev']
    + extras_require['test']
    + extras_require['lint']
)

setup(
    name='pretix-attestation-placeholder-plugin',
    version='0.2.1',
    description='Pretix Ethereum Plugin Developers',
    long_description=long_description,
    url='https://github.com/efdevcon/pretix-attestation-placeholder-plugin',
    author='Pretix Ethereum Plugin Developers',
    author_email='ticketing@devcon.org',
    license='MIT License',

    install_requires=[
        "pretix>=3.8.0",
        "urllib3<1.26.0",
    ],
    python_requires='>=3.6, <4',
    extras_require=extras_require,
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretix.plugin]
pretix_attestation_plugin=pretix_attestation_plugin:PretixPluginMeta
""",
)
