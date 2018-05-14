from setuptools import setup, find_packages

setup(
    name='pdrill',
    version='0.1',
    license='Apache License 2.0',
    packages=find_packages(),
    author='Kirill Kouzoubov',
    author_email='kirill.kouzoubov@ga.gov.au',
    description='Parallel Pixel Drill from S3 bucket, prototype/investigation',
    python_requires='>=3.5',
    install_requires=['numpy',
                      'rasterio',
                      'requests',
                      'botocore',
                      'boto3',
                      ],
    tests_require=['pytest'],
)
