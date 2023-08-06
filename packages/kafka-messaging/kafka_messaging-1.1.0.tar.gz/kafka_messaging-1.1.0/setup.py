import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kafka_messaging",
    version="1.1.0",
    author="Andre Ferrari Moukarzel",
    author_email="andremoukarzel@gmail.com",
    description="Simple interface for sending messages through Kafka",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/zaitt_computer_vision/kafka_api",
    packages=setuptools.find_packages(),
    install_requires=["confluent_kafka"],
    license="MIT",
    python_requires=">=3.6"
)