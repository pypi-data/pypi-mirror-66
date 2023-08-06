import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bot-da-os", # Replace with your own username
    version="0.0.1",
    author="Caio Costa",
    author_email="caugcosta@gmail.com",
    description="An AI library to handle CASD's service order requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/2020-mtp-03-grupo-09/bot-da-os",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
