from setuptools import find_packages, setup

setup(
    name='pyyaml-tags',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    use_scm_version={
        'version_scheme': 'guess-next-dev',
        'write_to': 'src/yaml_tags/__version__.py',
    },

    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',

    setup_requires=[
        'pytest-runner', 'setuptools_scm', 'setuptools_scm_git_archive'
    ],

    tests_require=['pytest'],
    test_suite='tests',

    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup',
    ],

)
