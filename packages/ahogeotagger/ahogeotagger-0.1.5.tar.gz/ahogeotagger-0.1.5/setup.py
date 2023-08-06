import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ahogeotagger", # Replace with your own username
    version="0.1.5",
    author='Yasser Bashir',
    author_email='yasser.bashir@arbisoft.com',
    description="Rapidly search your text for large list of cities and countries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ybashir/ahogeotagger",
    packages=['ahogeotagger'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'pyahocorasick==1.4.0',
    ],
    python_requires='>=3.6',
)
