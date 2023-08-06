from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="mgmail",
    entry_points={
        "console_scripts": [
            "mgmail_imp = mgmail.app.import_attachment:run",
        ],
    },
    version="1.1.0",
    author="Eugen Ciur",
    author_email="eugen@papermerge.com",
    url="https://github.com/papermerge/mg-mail",
    description=("Import document attachments from SMTP account"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2.0 License",
    keywords="SMTP, REST API, papermerge",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
