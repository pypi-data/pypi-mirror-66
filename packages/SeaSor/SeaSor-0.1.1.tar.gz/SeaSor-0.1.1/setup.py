import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(name='SeaSor',
        version='0.1.1',
        description='Search & Sorting algorithms',
        url='https://github.com/m1ghtfr3e/SearchSort',
        author='m1ghtfr3e',
        packages=setuptools.find_packages(),
        zip_safe=False,
        long_description = long_description,
        classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        ],
)
