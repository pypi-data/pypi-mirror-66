import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Kigo",
    version="0.0.11",
    author="Krzysztof Kaczkowski",
    author_email="krzysztof.kaczkowski@architekt-it.pl",
    description="Python framework for Event Async RPC",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/AsyncMicroStack/kigo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    extras_require={'docs': ["pyenchant==1.6.6",
                             "Sphinx==1.3",
                             "sphinxcontrib-spelling==2.1.1",
        ]
    }
)
