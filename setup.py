import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="drope",
    version="0.1.0",
    description="A utility for receiving file uploads",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jvstme/drope",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Communications :: File Sharing",
    ],

    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",

    entry_points={
        "console_scripts": [
            "drope=drope.cmdline:main",
        ],
    },

    install_requires=[
        "aiofiles ~= 0.8",
        "aiohttp ~= 3.8",
    ],

    extras_require={
        "dev": [
            "pytest",
            "pytest-aiohttp",
        ]
    },

    package_data={
        "": ["static/*"],
    },
    zip_safe=False,
)