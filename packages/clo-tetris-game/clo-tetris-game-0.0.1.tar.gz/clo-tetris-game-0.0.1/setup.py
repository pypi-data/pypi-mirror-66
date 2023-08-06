from setuptools import  setup, find_packages
import tetris_game

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="clo-tetris-game", 
    version=tetris_game.__version__,
    author="Cedric LOMBARD",
    author_email="cedric.lombard@cern.ch",
    description="A simple implementation of the Tetris Game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lombardc/tetris_game",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
       "pygame", "pillow"
   ],
   include_package_data=True,
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': [
            'playTetris = tetris_game.core:TetrisGame',
        ],
    },
)
