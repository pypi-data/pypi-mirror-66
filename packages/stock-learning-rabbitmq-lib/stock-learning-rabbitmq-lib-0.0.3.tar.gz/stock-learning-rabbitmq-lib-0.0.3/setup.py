import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stock-learning-rabbitmq-lib",
    version="0.0.3",
    author="Vinícius Luis da Silva",
    author_email="vinicius.lds.br@gmail.com",
    description="This is a package that includes all RabbitMQ handled messages by the stock-learning infrastructure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vinicius-lds/stock-learning-rabbitmq-lib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
