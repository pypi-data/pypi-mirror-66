"""
    Set up the sdc_helpers package
"""
from setuptools import setup


def get_required(file_name):
    with open(file_name) as f:
        return f.read().splitlines()


setup(
    name='sdc-helpers',
    packages=['sdc_helpers'],
    install_requires=get_required(file_name='./requirements.txt'),
    description='A Lambda Package for SDC Helpers',
    version='0.3',
    url='https://github.com/RingierIMU/sdc-global-all-helpers',
    author='Ringier South Africa',
    author_email='tools@ringier.co.za',
    keywords=['pip', 'lambda', 'helpers'],
    download_url='https://github.com/RingierIMU/sdc-global-all-helpers/archive/v0.3.zip'
)
