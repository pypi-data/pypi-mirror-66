from setuptools import setup, find_packages

setup(
    name = "mapclick",
    version = "0.1",
    install_requires=[
        'matplotlib',
        'numpy',
        'pyproj',
        'cartopy',
    ],
    url = 'https://github.com/xumi1993/mapclick',
    author = 'Mijian Xu',
    author_email = 'gomijianxu@gmail.com',
    packages = find_packages(), 
    package_dir = {'mapclick':'src'},
    include_package_data=True,
    zip_safe=False
)
