import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="star-lord",  # Replace with your own username
    version="0.0.1",
    description="Microservice with django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wienerdeming/star-lord",
    package_dir={'apps': 'assistant'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
