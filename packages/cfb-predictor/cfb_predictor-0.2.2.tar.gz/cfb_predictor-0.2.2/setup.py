from setuptools import setup, find_packages

setup(
    name="cfb_predictor",
    version="0.2.2",
    author="Steven Bischoff",
    author_email="steven.m.bischoff@gmail.com",
    description="Rates college football teams",
    url="https://github.com/sbischof/cfb_predictor",
    packages=find_packages(),
    install_requires=['pandas','numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
