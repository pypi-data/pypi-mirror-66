import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="terminal-pkg-Team3SP20",
    version="0.0.7",
    author="Team3SP20",
    author_email="dansharp94@mail.mvnu.edu",
    description="Files for cafeteria terminal prototype",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MVNUCS/TeamThreeSP20",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)