import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'getgdelt',
    version="0.0.1",
    author='Sun Yufei',
    author_email='syfyufei@gmail.com',
    description='Get and use gdelt data more reliably without hardware limitation.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/syfyufei/getgdelt',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
