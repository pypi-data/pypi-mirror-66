import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='buildflaskapp',  
    version='0.0.1.1.1',
    author="Hans Maulloo",
    author_email="askyourkode@gmail.com",
    description="Generate flask app boilerplate!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/askyourkode/buildflaskapp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Freely Distributable",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["buildflaskapp=buildflaskapp.buildflaskapp:main"]}
)
