import setuptools

with open("README.md", "r") as f:
    long_desc = f.read()

setuptools.setup(
    name="pash-cmd",
    version="0.0.1",
    author="MattMoony",
    author_email="m4ttm00ny@gmail.com",
    description="An interactive shell for Python scripts.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/MattMoony/pash",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'colorama==0.4.3',
    ],
    python_requires='>=3.7',
)