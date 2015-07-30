from distutils.core import setup

setup(
    name='deployer_lite_server',
    version='0.0.1',
    packages=[''],
    url='https://github.com/harnash/deployer-lite',
    license='Apache 2',
    author='£ukasz Harasimowicz',
    author_email='dev@harnash.eu',
    description='',
    tests_require=[
        'nose==1.3.7',
    ],
    install_requires=[
        'pyzmq==14.7.0',
        'click==4.1',
    ]
)
