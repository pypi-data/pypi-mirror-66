import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="avery-Trading-ML",
    version="0.8.0",
    author="Avery Pustina",
    author_email="author@example.com",
    description="Utility for analyzing stock market data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=["avery_Trading_ML"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["yfinance", "pandas", "numpy"],
    python_requires='>=3.6',
)