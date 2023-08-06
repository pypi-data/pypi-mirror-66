import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_mscip",
    version="0.1.0",
    author="Memsense",
    author_email="nneisen@memsense.com",
    description="Library interface for communication with Memsense IMU devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/memsense/py_mscip",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",],
    python_requires=">=3.6",
)
