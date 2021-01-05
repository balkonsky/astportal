import io
import re

from setuptools import setup

# with io.open('README.md', 'rt', encoding='utf8') as f:
#     readme = f.read()

with io.open('src/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='astportal',
    version=version,

    license='MIT',
    description='Automation Platform powered by Flask',
    # long_description=readme,
    long_description_content_type='text/markdown',

    author='Maksim Avramenko',
    author_email='MAvramenko@humans.net',

    platforms=['any'],
    install_requires=[
        'flask >= 1.0.2',
        'flask_cors >= 3.0.6',
        'flask_sqlalchemy >= 2.3.2',
        'flask_jwt_extended >= 3.12.1',
        'python-dotenv >= 0.9.1',
        'rq >= 0.12.0',
        'cerberus >= 1.2',
        'rq-scheduler >= 0.8.3',
        'ldap3>=2.6.1',
        'PyMySQL>=0.9.3'
    ],
    setup_requires=[],
    tests_require=[],
    extras_require={},
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'src = src.cli:cli'
        ]
    },
    packages=['kitchen'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
