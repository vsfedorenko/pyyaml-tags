import io
from os.path import abspath, dirname, join
from shutil import rmtree

from setuptools import find_packages, setup

root_dir = abspath(dirname(__file__))

dist_dir = join(root_dir, 'dist')
build_dir = join(root_dir, 'build')

src_dir = join(root_dir, 'src')
package_dir = join(src_dir, 'yaml_tags')


def cleanup():
    rmtree(build_dir, ignore_errors=True)
    rmtree(dist_dir, ignore_errors=True)


def get_about():
    with io.open(join(package_dir, '__about__.py'), encoding='utf-8') as f:
        about = {}
        exec(f.read(), about)
    return about


def setup_package():
    cleanup()

    about = get_about()

    setup(
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

        name=about['__title__'],
        description=about['__summary__'],
        author=about['__author__'],
        author_email=about['__email__'],
        url=about['__uri__'],
        license=about['__license__'],

        classifiers=[
            'License :: OSI Approved :: MIT License',
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


if __name__ == '__main__':
    setup_package()
