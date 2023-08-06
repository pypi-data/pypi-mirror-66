import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nlptxtools",
    version="0.0.1",
    author="Midriaz",
    author_email="scome@inbox.ru",
    description="NLP tools for Russian language",
    url="https://github.com/Midriaz/nlptxtools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.6'
)
