import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="factiva_country_code_mapping",
    author="Supearnesh",
    version="1.0.1",
    author_email="arnesh.sahay@gmail.com",
    description="A utility to simplify mapping Factiva country codes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Supearnesh/factiva-country-code-mapping",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)