import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="terminal-pkg-Team3SP20",
    version="1.0.1",
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
    package_data={
        "": ["*.mp3", "*.wav"] 
    },
    include_package_data=True,
)