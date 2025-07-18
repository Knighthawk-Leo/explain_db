from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="explain_db",
    version="0.1.0",
    author="Sanskar Dwivedik",
    author_email="sanskardwivedi003@gmail.com",
    description="A Django package to expose model metadata via API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/explain_db",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=3.2",
        "djangorestframework>=3.12.0",
    ],
    keywords="django, model, metadata, api, database",
    include_package_data=True,
    zip_safe=False,
) 