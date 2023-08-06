from setuptools import setup

setup(
    name='gopro2gpx',
    version='0.1',
    packages=['gopro2gpx'],
    url='',
    license='',
    author='raphaelcourivaud',
    author_email='r.courivaud@gmail.com',
    description='',
    entry_points={
        'console_scripts': [
            'extract_gps=gopro2gpx.main:main',
        ],
    }
)
