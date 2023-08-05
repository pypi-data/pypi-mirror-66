import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="domestic_violence_news_classifer_spanish",
    version="0.0.2",
    author="Hugo J. Bello",
    author_email="hjbello.wk@gmail.com",
    description="A classifier for domestic violence newspaper news in spanish",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/domestic-violence-ai-studies/domestic-violence-news-classifier-spanish",
    packages=setuptools.find_packages(),
    package_data={'domestic_violence_news_classifer_spanish': ['saved_models/*']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)