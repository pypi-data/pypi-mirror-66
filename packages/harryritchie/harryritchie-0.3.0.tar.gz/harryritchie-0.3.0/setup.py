import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="harryritchie", # Replace with your own username
    version="0.3.0",
    author="Harry Ritchie",
    author_email="harry.ritchie@prea.eu",
    description="A package for geo tools used to map card score",
    url="https://github.com/pypa/sampleproject",
    packages=["GeoFuns"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements
)
