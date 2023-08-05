import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="compete",
    version="0.0.1",
    author="Pragy Agarwal",
    author_email="agar.pragy@gmail.com",
    description="Competitive Coding in Python!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ScalerAcademy/py-compete",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
