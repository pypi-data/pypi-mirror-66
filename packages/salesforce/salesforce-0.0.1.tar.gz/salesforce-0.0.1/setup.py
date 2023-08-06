import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="salesforce", # Replace with your own username
    version="0.0.1",
    author="Will Watkinson",
    author_email="wjwats4295@gmail.com",
    description="A package to perform API calls to Salesforce",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/wjwatkinson/salesforce",
    packages=["salesforce"],
    install_requires=['simple-salesforce', 'requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
