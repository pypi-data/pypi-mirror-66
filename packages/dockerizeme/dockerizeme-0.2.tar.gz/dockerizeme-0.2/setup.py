from setuptools import setup, find_packages

setup(
    name='dockerizeme',
    version='0.2',
    packages=find_packages(),
    py_modules=['dockerizeme'],
    description ='Generate Dockerfile for your project automatically',
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'dockerizeme=package.dockerize:cli'
        ]
    },
    zip_safe=False,
    include_package_data=True
)