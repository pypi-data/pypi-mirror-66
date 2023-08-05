import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="calibrated",  # Replace with your own username
    version="0.0.1",
    author="Anshul Gupta",
    author_email="anshulgupta217@gmail.com",
    description="This middleware gives same structure in django success and error case.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anshul217/calibrated",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
