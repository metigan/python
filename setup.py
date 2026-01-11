from setuptools import setup, find_packages

setup(
    name="metigan",
    version="1.0.5",
    description="Official Metigan SDK for Python - Email, Forms, Contacts, and Audiences management",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Metigan",
    author_email="support@metigan.com",
    url="https://github.com/metigan/python",
    project_urls={
        "Homepage": "https://metigan.com",
        "Documentation": "https://docs.metigan.com",
        "Repository": "https://github.com/metigan/python",
        "Issues": "https://github.com/metigan/python/issues",
    },
    packages=find_packages(exclude=["tests", "examples"]),
    install_requires=[
        "requests>=2.31.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    license="MIT",
    include_package_data=True,
)

