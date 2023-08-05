import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sphinx2doxygen",
    version="0.1",
    scripts=['sphinx2doxygen'],
    license='EUPL-1.2',
    author="Brolf",
    author_email="brolf@magheute.net",
    description="Rewrites python documentation string code commenting from Sphinx to Doxygen format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/br-olf/sphinx2doxygen",
    keywords=['PEP', 'convert', 'Doxygen', 'Google'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development :: Documentation",
        "Development Status :: 3 - Alpha"
    ],
    python_requires='>=3.6',
)
