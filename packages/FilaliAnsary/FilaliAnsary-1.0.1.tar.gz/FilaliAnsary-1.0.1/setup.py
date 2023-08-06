from setuptools import setup

with open("README.md","r") as fh :
    ld=fh.read()


setup(
    name="FilaliAnsary",
    version="1.0.1",
    description="A Python package created to kill time.",
    long_description=ld,
    long_description_content_type="text/markdown",
    author="Abdelouahab FILALI ANSARY",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    install_requires=["requests"],
    package_dir={'': "2"},
    py_modules=["Ansary","EE"],
    extras_require = {"dev" : ["pytest>= 3.7",],},


)