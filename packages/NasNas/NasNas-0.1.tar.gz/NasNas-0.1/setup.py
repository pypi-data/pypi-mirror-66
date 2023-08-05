from setuptools import setup, find_packages

with open("readme.md", "r") as rdme:
    long_description = rdme.read()


setup(
    name="NasNas",
    version="0.1",
    author="Modar Nasser",
    author_email="modar1999@gmail.com",
    description="A simple game framework to get started quickly with python and sfml.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Madour/NasNas",
    package_dir={'NasNas': 'src/NasNas'},
    install_requires=['sfml>=2.3'],
    packages=find_packages(where='src'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3"
    ]
)