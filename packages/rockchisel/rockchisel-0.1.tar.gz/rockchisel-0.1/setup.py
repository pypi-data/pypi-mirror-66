
import setuptools

setuptools.setup(
    name="rockchisel", # Replace with your own username
    version="0.1",
    author="Michael DeHaan",
    author_email="michael@michaeldehaan.net",
    description="A static documentation/website generator",
    long_description="RockChisel is a static documentation and website generator.",
    long_description_content_type="text/plain",
    url="https://rockchisel.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
	    "Operating System :: MacOS :: MacOS X",
	    "Topic :: Documentation"
    ],
    python_requires='>=3.6',
)
