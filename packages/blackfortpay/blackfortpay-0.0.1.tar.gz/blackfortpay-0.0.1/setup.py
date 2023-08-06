import setuptools

def parse_requirements(filename):
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blackfortpay",
    version="0.0.1",
    author="panwaclaw",
    author_email="vkozlovsk@gmail.com",
    description="BlackFort Payment API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/panwaclaw/blackfortpay",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=parse_requirements('requirements.txt'),
)