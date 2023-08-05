import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyDX-DevWorks8",  # Replace with your own username
    version="1.0.0",
    author="Christian Lachapelle",
    author_email="devworks8@gmail.com",
    description="Flatten and inflate a dictionary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Devworks8/PyDX.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)