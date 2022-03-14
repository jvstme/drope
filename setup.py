import setuptools

setuptools.setup(
    name="drope",
    version="0.1.0",
    description="A script to receive file uploads",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    zip_safe=False,

    entry_points={
        "console_scripts": [
            "drope=drope.cmdline:main",
        ],
    },

    install_requires=[
        "aiofiles",
        "fastapi",
        "python-multipart",
        "uvicorn",
    ],

    extras_require={
        "dev": [
            "pytest",
            "requests",
        ]
    }
)