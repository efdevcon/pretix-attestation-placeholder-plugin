import os
from distutils.command.build import build

from setuptools import find_packages, setup


try:
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = ''


class CustomBuild(build):
    def run(self):
        from django.core import management
        management.call_command('compilemessages', verbosity=1)
        build.run(self)


cmdclass = {
    'build': CustomBuild
}


setup(
    name='pretix-attestation-placeholder-plugin',
    version='0.1.0',
    description='Pretix Ethereum Plugin Developers',
    long_description=long_description,
    url='https://github.com/efdevcon/pretix-attestation-placeholder-plugin',
    author='Pretix Ethereum Plugin Developers',
    author_email='Your email',
    license='MIT License',

    install_requires=[
        "pretix>=3.8.0",
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretix.plugin]
pretix_attestation_plugin=pretix_attestation_plugin:PretixPluginMeta
""",
)
