# setup.py
from setuptools import setup, find_packages

setup(
    name='project-monarch',
    version='1.0.0',
    packages=find_packages(), # Should find monarch_core
    install_requires=[
        'openai',
        'python-dotenv',
        'google-search-results',
        'chromadb',
        'sentence-transformers',
    ],
    entry_points={
        'console_scripts': [
            # Points to the main function inside monarch_core/cli.py
            'monarch = monarch_core.cli:main',
        ],
    },
)