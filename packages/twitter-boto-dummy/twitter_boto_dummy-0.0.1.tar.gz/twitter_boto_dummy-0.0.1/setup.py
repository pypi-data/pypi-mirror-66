import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="twitter_boto_dummy",
    version="0.0.1",
    author="sammer sallam",
    author_email="samersallam92@gmail.com",
    description="This library is to help you have a twitter bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Samer92/twitter_boto_dummy",
    packages=["twitter_boto_dummy"],
    install_requires=["aws-s3-resource==0.0.2","boto3==1.12.43","botocore==1.15.43","certifi==2020.4.5.1",
                      "chardet==3.0.4","docutils==0.15.2","idna==2.9","jmespath==0.9.5",
                      "langdetect==1.0.8","numpy==1.18.3","oauthlib==3.1.0","pandas==1.0.3",
                      "PySocks==1.7.1","python-dateutil==2.8.1","pytz==2019.3",
                      "requests==2.23.0","requests-oauthlib==1.3.0","s3transfer==0.3.3",
                      "six==1.14.0","tweepy==3.8.0","urllib3==1.25.9"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)