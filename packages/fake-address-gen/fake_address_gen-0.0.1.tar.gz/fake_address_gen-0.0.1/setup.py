import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fake_address_gen", # Replace with your own username
    version="0.0.1",
    author="Bishal Sarangkoti",
    author_email="sarangbishal@gmail.com",
    description="A small example package to generate fake data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bishalsarang/fake-address-generator",
    packages=["fake_address_gen"],
    install_requires=["requests", "bs4"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)