import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stackpeanut", # Replace with your own username
    version="0.0.3",
    author="Isara_stackpython",
    author_email="author@example.com",
    description="a package that contain my lovely peanut",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires= ['numpy'],
    python_requires='>=3.6',
)