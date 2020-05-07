from setuptools import setup

setup(
    name='easy_elastic',
    version='0.1.0',
    description='A Python package for elasticsearch',
    url='https://github.com/surajptl/simple_elastic',
    author='Suraj Patel',
    author_email='suraj326len@gmail.com',
    license='BSD 2-clause',
    packages=['easy_elastic'],
    install_requires=['elasticsearch'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
	'Programming Language :: Python :: 3.6',
	'Programming Language :: Python :: 3.7',
    ],
)
