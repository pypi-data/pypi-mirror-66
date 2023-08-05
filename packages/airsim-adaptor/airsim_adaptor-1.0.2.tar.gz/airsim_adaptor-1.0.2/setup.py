import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airsim_adaptor", # Replace with your own username
    version="1.0.2",
    author="ibrahim aydin",
    author_email="noemail@sorry.com",
    description="A customized airsim API adaptor for special purposes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ibrahim0v",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)