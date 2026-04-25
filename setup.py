# Developer: Vishal Raj V, Senior Engineer
from setuptools import setup, find_packages

setup(
    name='oh-my-gemini-slim',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'omg=oh_my_gemini_slim.cli:main',
        ],
    },
)
