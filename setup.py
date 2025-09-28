# setup.py
from setuptools import setup

setup(
    name='project-monarch',
    version='1.0.0',
    py_modules=['main', 'agent', 'monarch', 'job', 'tools', 'memory'],
    install_requires=[
        'openai',
        'python-dotenv',
        'google-search-results',
        'chromadb',
        'sentence-transformers',
    ],
    entry_points={
        'console_scripts': [
            'monarch = main:main',
        ],
    },
)