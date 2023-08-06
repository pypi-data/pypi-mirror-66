import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="protein", # Replace with your own username
    version="0.0.1",
scripts=['protein.py'],
    author="ctsahn",
    author_email="ctsahn@gmail.com",
    description="Test protein package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ctsahn/NBAPredict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)