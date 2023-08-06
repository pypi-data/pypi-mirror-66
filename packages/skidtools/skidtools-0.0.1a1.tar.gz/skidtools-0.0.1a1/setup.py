import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skidtools", # Replace with your own username
    version="0.0.1a1",
    author="Abdos",
    author_email="admin.dev@clast.dev",
    description="A small utility package to reduce boilerplate code in skid scripts",
    long_description= long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Abd0s/skidtools/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Topic :: Utilities",
        "Typing :: Typed"
    ],
    python_requires='>=3.6',
)