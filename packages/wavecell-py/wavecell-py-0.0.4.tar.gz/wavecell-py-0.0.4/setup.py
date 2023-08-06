import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wavecell-py",
    version="0.0.4",
    author="Saggaf Arsyad",
    author_email="saggaf@nbs.co.id",
    description="Wavecell REST API Wrapper for Python",
    license="MIT",
    long_description="Provide SMS and Mobile Verification integration for Python apps",
    long_description_content_type="text/markdown",
    url="https://github.com/saggafarsyad/wavecell-python",
    packages=setuptools.find_packages(),
    install_requires=[
        'phonenumbers',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
