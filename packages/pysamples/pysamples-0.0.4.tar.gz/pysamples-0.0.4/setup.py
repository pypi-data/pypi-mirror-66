import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read().replace("  ", "\n", -1)

setuptools.setup(
    name="pysamples",
    version="0.0.4",
    author="Dejian Meng",
    author_email="medean@live.cn",
    description="Python samples package",
    long_description=long_description,
    url="https://github.com/mdjdot/pysamples",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
