import io

import setuptools

entry_points = {
    "console_scripts": [
        "smn = smn.cli:main",
    ]
}

with io.open("requirements.txt", "rt", encoding="utf-8") as f:
    requires = [i for i in f.read().splitlines() if i]


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smn",
    version="0.0.7",
    author="Xuehua Xu",
    author_email="xuxuehua3@gmail.com",
    description="Share My Notebook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="notebook, knowledge base",
    license="MIT License",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requires,
    entry_points=entry_points,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)