from setuptools import setup
from setuptools import find_packages
from auth import __version__


setup(
    name='ky-auth-utils',
    version=__version__,
    packages=find_packages(),
    extras_require={
        "flask": ["flask"],
    },
    zip_safe=False,
    platforms='any'
)
