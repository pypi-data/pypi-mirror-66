from distutils.core import setup

setup(
    name='gistat',
    packages=['gistat'],
    version='v0.2.1',
    license='apache-2.0',
    description='Parsing https://gismoldova.maps.arcgis.com statistics related to covid-19 (Coronavirus)',
    author='Alex H.',
    author_email='alexander.habasescu@gmail.com',
    url='https://github.com/alexkingdom/gistat',
    download_url='https://github.com/alexkingdom/gistat/archive/v0.2.1.tar.gz',
    keywords=['covid-19 statistics', 'Moldova covid-19', 'Parser gismoldova'],
    install_requires=[
        'selenium',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
