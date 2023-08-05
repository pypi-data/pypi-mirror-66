import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Covid19ApiWrapper", 
    version="0.0.4",
    author="Aero",
    author_email="support@host-info.net",
    description="A basic API wrapper to interact with https://corona.lmao.ninja/.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aerobotpro/covid-19-data-utils/tree/master/src/py/covid-19-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
