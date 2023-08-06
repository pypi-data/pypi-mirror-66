from distutils.core import setup

setup(
    name="pysho",
    version="0.0.2",
    description="A Pure python shell",
    author="Ian Norton",
    author_email="inorton@gmail.com",
    url="https://gitlab.com/cunity/pysho",
    packages=["pysho"],
    platforms=["any"],
    license="License :: OSI Approved :: MIT License",
    long_description="A python based shell",
    install_requires=["pyreadline", "ptpython"],
    entry_points={
        "console_scripts": [
            "pysho = pysho.__main__:main"
        ]
    }
)
