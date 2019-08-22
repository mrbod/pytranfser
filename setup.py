from setuptools import setup

name = 'pytransfer'
version = '1.0.0'

setup(
    name=name,
    version=version,
    description='upload to transfer.sh',
    author='Per Forser',
    author_email='per.forser@gmail.com',
    url='file:///pytransfer.tar.gz',
    packages=['pytransfer'],
    python_requires='>=3.6',
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'transfer=pytransfer.transfer:main',
        ],
    }
)

