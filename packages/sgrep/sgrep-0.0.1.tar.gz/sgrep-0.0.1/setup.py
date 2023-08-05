import setuptools

setuptools.setup(
    name="sgrep",
    version="0.0.1",
    author="Drew Dennison",
    author_email="drew@returntocorp.com",
    description="A python package of sgrep tool",
    url="https://sgrep.dev",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)