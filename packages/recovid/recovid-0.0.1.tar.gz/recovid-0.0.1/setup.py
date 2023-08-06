import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
    name='recovid',
    version='0.0.1',
    author="Amr Kayid",
    author_email="amrmkayid@gmail.com",
    description="Researching COVID-19 Open Research Dataset Challenge (CORD-19)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amrmkayid/recovid",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
