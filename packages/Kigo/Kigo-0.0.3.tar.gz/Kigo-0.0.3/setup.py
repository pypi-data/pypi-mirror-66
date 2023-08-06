import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Kigo",
    version="0.0.3",
    author="Krzysztof Kaczkowski",
    author_email="krzysztof.kaczkowski@architekt-it.pl",
    description="Python framework for Event Async RPC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AsyncMicroStack/kigo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
