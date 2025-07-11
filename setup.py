from setuptools import setup, find_packages

setup(
    name="pypop",
    version="1.0",
    packages=find_packages(),  # include gui/, core/, etc.
    install_requires=["requests"],
    entry_points={
        'console_scripts': [
            'pypop = run:main',
        ],
    },
)

