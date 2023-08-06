import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
        name='istar_m9csz_core',
        version='0.0.7',
        author="Matt O'Tousa",
        author_email='motousa@pdx.edu',
        description='Core M9CSZ data parsing',
        long_description_content_type='text/markdown',
        url='https://github.com/Tattomoosa/m9csz',
        packages=setuptools.find_packages(),
        # data_files=[
            # ('appdata', ['istar_m9csz_core/appdata/*.json'])
            # ],
        install_requires=[
            'cftime', 'dask', 'netCDF4', 'numpy', 'pandas',
            'six', 'xarray', 'pytz', 'six'
            ],
        include_package_data=True,
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            ],
        python_requires='>=3.7')
