import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymp",
    version="0.0.2",
    author="Michael J Tallhamer MSc DABR",
    author_email="mike.tallhamer@gmail.com",
    description="A small package of medical physics toys",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tallhamer/pymp",
    packages=setuptools.find_packages(),
    package_data={'pymp': ['test/*.py', 'data/*', 'data/wl/*']},
    install_requires=[
        "numpy >= 1.16.3",
        "scipy >= 1.3.0",
        "pandas >= 0.25.0",
        "numba >= 0.48.0"
        "pytest"
     ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
