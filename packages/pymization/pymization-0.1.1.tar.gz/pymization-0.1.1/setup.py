import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="pymization",
    version="0.1.1",
    packages=["pymization"],
    license="MIT",
    author="Nicolas Camus & Maurice Poirrier",
    author_email="maurice@merkenlabs.com",
    description="A simple optimization solverp problem",
    download_url="https://github.com/mauricepoirrier/pymization/archive/0.0.1.tar.gz",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mauricepoirrier/pymization",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy",],  # I get to this in a second
)
