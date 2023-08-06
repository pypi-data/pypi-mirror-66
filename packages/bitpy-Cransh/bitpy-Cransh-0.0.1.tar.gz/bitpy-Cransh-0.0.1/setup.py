import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bitpy-Cransh", # Replace with your own username
    version="0.0.1",
    author="Cransh",
    author_email="Cransh.t2.2t.hsnrc@gmail.com",
    description="enhanced Bool Object",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cransh/bitpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)