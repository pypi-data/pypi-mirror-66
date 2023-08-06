import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simpletexting",
    version="0.0.1",
    author="Tom Boswick",
    author_email="taboswick@example.com",
    description="A Python Module for Simple Texting's API",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://github.com/tboswick/Simple-Texting",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['Simple Texting'],
    #packages=['simpletexting'],
    python_requires='>=3.6',
    install_requires=[
          'xmltodict',
          'requests',
      ],
)
