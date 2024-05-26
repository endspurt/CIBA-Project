from setuptools import setup, find_packages

setup(
    name='CIBAProject',
    version='0.1',
    packages=find_packages(),
    # package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'ciba_project=src.__main__:main_bot',
        ],
    },
)