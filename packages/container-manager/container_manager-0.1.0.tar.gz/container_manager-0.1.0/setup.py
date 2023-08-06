import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
def _requires_from_file(filename):
    return open(filename).read().splitlines()

setuptools.setup(
    name="container_manager",
    version="0.1.0",
    description="Container manager",
    author='YujiOshima',
    author_email='yuji.oshima0x3fd@gmail.com',
    maintainer='YujiOshima',
    maintainer_email='yuji.oshima0x3fd@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YujiOshima/container_manager",
    install_requires=_requires_from_file('requirements.txt'),
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['coctl = container_manager.coctl:main']
    },
    python_requires='>=3.7',
)
