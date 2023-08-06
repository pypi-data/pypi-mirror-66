import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BoltRP",  # Replace with your own username
    version="0.0.1",
    author="Johan Medrano",
    author_email="johan.medrano@umontpellier.fr",
    description="Torch-powered RQA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yop0/BoltRP",
    packages=setuptools.find_packages(),
    install_requires=[
        'torch',
        'torchvision',
        'numpy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license='MIT'
)
