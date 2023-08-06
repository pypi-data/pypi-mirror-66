import setuptools

with open("PIP.md", "r") as f:
    long_description = f.read();

setuptools.setup(
    name="tgbf",
    version="0.0.2",
    author="Mike",
    author_email="mike@mikey.ir",
    description="Telegram Bot Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WiGeeky/TGBotFramework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
)
