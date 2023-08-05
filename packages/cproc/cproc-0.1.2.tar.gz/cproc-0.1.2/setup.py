import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cproc",
    version="0.1.2",
    author="Jakob Simon-Gaarde",
    author_email="jakobsg@simon-gaarde.dk",
    description="A small tool to capture the environment of a running process",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/jakobsg/cproc",
    packages=setuptools.find_packages(),
    scripts=[
        'scripts/cproc',
        'scripts/rproc'],
install_requires=[
        'psutil'
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6',
)
