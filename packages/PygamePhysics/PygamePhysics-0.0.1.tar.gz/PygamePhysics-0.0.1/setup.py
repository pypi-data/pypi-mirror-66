import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PygamePhysics", # Replace with your own username
    version="0.0.1",
    author="Ethan Culp",
    author_email="ethan.culp101@gmail.com",
    description="Help with physics in Pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SeventyFox92475/pygamePhysics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)