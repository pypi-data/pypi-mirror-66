import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topsis_by_siddhant", # Replace with your own username
    version="1.0.0",
    author="Siddhant Khurana",
    author_email="siddhantkhurana10@gmail.com",
    description="A package for Topsis technique",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['topsis'],
    install_requires=[
       'numpy','pandas','scipy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)