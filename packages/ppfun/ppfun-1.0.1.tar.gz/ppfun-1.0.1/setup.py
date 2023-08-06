import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ppfun",
    version="1.0.1",
    author="portasynthinca3",
    author_email="portasynthinca3@gmail.com",
    description="Allows you to use the PixelPlanet.Fun API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/portasynthinca3/ppfun",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Freeware",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
    ],
    python_requires='>=3.6',
)
