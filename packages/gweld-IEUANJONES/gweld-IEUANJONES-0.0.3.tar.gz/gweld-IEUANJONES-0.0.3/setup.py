import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='gweld-IEUANJONES',
    version='0.0.3',
    author='Ieuan Jones',
    author_email='ieujon@googlemail.com',
    description='A simple charting library',
    long_description=long_description,
    url='https://github.com/ieuanjones/gweld',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
    install_requires=['lxml']
)
