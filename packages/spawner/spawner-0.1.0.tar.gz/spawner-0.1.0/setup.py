from setuptools import setup, find_packages  # noqa: H301

NAME = "spawner"
VERSION = "0.1.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    author="Spawner Team",
    author_email="info@spawner.ai",
    name=NAME,
    version=VERSION,
    description="Spawner API",
    url="https://github.com/spawner/python-sdk",
    keywords=["Spawner", "Python", "API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Welcome to the Spawner API! 
    """,
    
    classifiers=[
    'Development Status :: 3 - Alpha',   
    'Intended Audience :: Developers',     
    ],
)