from setuptools import setup, find_packages

setup(
    name="PyRoPy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "tcod>=15.0.0",
        "numpy>=1.24.0",
    ],
    python_requires=">=3.12",
    author="Martijn Schut",
    description="A roguelike game written in Python using the tcod library",
    keywords="roguelike, game, tcod",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
) 