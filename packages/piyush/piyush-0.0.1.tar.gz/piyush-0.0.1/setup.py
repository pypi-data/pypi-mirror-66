from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(

    name='piyush',
    version='0.0.1',
    description='hi piyush',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Piyush Lakhani",
    author_email="elearning.piyush@gmail.com",
    url="https://github.com/phlakhani/GitUploader",
    py_modules=['piyush'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 8.1",
    ],
    python_requires='>=3.6',
)
