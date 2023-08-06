from setuptools import find_packages, setup


def reamde_to_long_description():
    """Convert README.md to long description for PYPI"""
    with open("README.md", encoding="UTF-8") as readme_file:
        readme = readme_file.readlines()

    html_start = min(ix for ix, line in enumerate(readme) if "<p>" in line)
    html_stop = max(ix for ix, line in enumerate(readme) if "</p>" in line)
    readme = [
        line
        for ix, line in enumerate(readme)
        if ix not in range(html_start, html_stop + 1)
    ]
    long_description = "\n".join(readme)
    print(long_description)
    return long_description


DEV_REQUIRES = [
    "black",
    "pylint",
    "pre-commit",
    "mypy",
    "sqlalchemy-stubs",
    "pytest",
    "pytest-cov",
    "mkdocs",
]

setup(
    name="alembic_utils",
    version="0.1.4",
    author="Oliver Rice",
    author_email="oliver@oliverrice.com",
    license="MIT",
    description="A sqlalchemy/alembic extension for migrating procedures and views ",
    python_requires=">=3.7",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["alembic", "psycopg2-binary", "flupy", "sqlalchemy", "parse"],
    extras_require={
        "dev": DEV_REQUIRES,
        "nvim": ["neovim", "python-language-server"],
        "docs": ["mkdocs", "pygments", "pymdown-extensions"],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: SQL",
    ],
)
