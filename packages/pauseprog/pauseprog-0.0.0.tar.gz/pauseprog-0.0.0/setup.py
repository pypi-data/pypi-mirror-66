import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pauseprog",
    author="pechenzZ",
    author_email="nikolayakimovich8@gmail.com",
    description="A small package to pause your beautiful program!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pechenzz/pauseprog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)