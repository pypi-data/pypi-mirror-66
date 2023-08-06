import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="pwbus",
    version="0.0.3",
    author="Fabio Szostak",
    author_email="fszostak@gmail.com",
    description="A simple task execution manager with integration bus cababities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fszostak/pwbus",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)
