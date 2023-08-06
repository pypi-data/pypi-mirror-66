import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stack_noodle", # Replace with your own username
    version="0.0.3",
    author=["Isarafx","My lovely duck"],
    author_email="isarawn@gmail.com",
    description="Everyone love noodle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires='numpy',
)
