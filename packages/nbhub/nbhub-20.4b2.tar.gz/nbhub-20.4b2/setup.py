import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nbhub",
    version="20.4b2",
    author="Duarte O.Carmo",
    author_email="duarteocarmo@gmail.com",
    description="Publish jupyter notebooks from the command line.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="jupyter notebook cli sharing",
    url="https://github.com/duarteocarmo/nbhub",
    install_requires=["click", "requests"],
    py_modules=["nbhub"],
    entry_points={"console_scripts": ["nbhub=nbhub:main",]},
    extras_require={"test": ["coverage", "pytest"],},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    project_urls={
        "Bug Reports": "https://github.com/duarteocarmo/nbhub/issues",
        "Say Thanks!": "https://nbhub.duarteocarmo.com",
        "Source": "https://github.com/duarteocarmo/nbhub",
    },
)
