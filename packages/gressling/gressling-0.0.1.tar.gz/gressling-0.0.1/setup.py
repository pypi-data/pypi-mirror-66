import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gressling", # Replace with your own username
    version="0.0.1",
    author="Gressling, T.",
    author_email="mail@gressling.com",
    description="Implementation of an data science assistance framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gressling/index",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)