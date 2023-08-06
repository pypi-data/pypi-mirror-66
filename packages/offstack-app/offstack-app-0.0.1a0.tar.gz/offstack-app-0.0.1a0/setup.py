"""setup.py: setuptools control."""



from setuptools import setup
from offstack.constants import VERSION

long_descr = """
Locally store your Stackoverflow favorites, without the need to constantly look them up. Works only on Linux machines.

For further information and a usage guide, please view the project page:

https://github.com/calexandru2018/offstack-app
"""

setup(
    name="offstack-app",
    packages=["offstack"],
    entry_points={
        "console_scripts": ["offstack = offstack.__main__:init"]     
    },
    include_package_data=True,
    version=VERSION,
    description="Offline store favorite marked questions and answers from Stackoverflow.",
    long_description=long_descr,
    author="calexandru2018",
    license="GPLv3",
    url="https://github.com/calexandru2018/offstack-app",
    install_requires=[
        "requests",
        "requests-oauthlib",
        "oauthlib",
        "setuptools",
        "selenium",
    ],
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: X11 Applications",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
