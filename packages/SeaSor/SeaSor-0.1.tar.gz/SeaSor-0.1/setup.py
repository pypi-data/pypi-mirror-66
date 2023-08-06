import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(name='SeaSor',
        version='0.1',
        description='Search & Sorting algorithms',
        url='https://github.com/m1ghtfr3e/SearchSort',
        author='m1ghtfr3e',
        packages=setuptools.find_packages(),
        zip_safe=False,
        long_description = long_description,
        classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: Other/Proprietary License',
        ],
)
