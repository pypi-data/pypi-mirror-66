import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spongebox",  # 届时使用pip install {}的包名
    version="0.1.0",
    author="spongebob23",
    author_email="947022718@qq.com",
    description="A high-level wrapped tool-chest within frequently used functionalities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
