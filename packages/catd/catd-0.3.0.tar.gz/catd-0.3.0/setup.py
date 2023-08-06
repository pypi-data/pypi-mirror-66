import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="catd",
    version="0.3.0",
    author="Wang Qin",
    author_email="danielqin7@outlook.com",
    description="A Chinese co-word analysis with topic discovery package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dqwerter/catd",
    download_url='https://github.com/dqwerter/catd/archive/0.3.0.tar.gz',
    packages=setuptools.find_packages(),
    install_requires=[  # I get to this in a second
        'jieba',
        'gensim',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
