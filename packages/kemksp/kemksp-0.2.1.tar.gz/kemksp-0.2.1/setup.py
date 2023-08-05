import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kemksp", # Replace with your own username
    version="0.2.1",
    author="Kontiko",
    author_email="kontiko.fb@gmail.com",
    description="A package to manage your KSP Addons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kontiko/Kerbal-Extension-Manager",
    packages= ["kemksp"],
    package_data={"kemksp":["config.json"]},
    entry_points = {
        'console_scripts': [
            'kem = kemksp.kemterminal:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
) 

