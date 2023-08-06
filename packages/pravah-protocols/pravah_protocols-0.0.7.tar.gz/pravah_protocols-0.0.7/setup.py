import setuptools

setuptools.setup(
    name="pravah_protocols",
    version="0.0.7",
    author="Abhishek Upperwal",
    author_email="mesh@soket.in",
    description="Proto generated for all protocols",
    url="https://github.com/pravahio",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'protobuf'
    ]
)