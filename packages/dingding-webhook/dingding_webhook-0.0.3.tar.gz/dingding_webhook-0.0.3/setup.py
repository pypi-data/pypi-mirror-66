import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dingding_webhook", # Replace with your own username
    version="0.0.3",
    author="nowindxdw",
    author_email="nowindxdw@126.com",
    description="A simple api for dingding robot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nowindxdw/dingdingwebhook",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)