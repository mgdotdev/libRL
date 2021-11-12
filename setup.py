import os.path
from setuptools import setup, find_packages, Extension

extensions = [
    Extension(
        "libRL.tools._extensions",
        [os.path.join("src", "libRL", "tools", "_extensions.cpp")],
    )
]

here = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="libRL",
    version="2.0.0",
    python_requires=">=3.6",
    include_package_data=True,
    description="Python library for characterizing Microwave Absorption",
    long_description=long_description,
    url="https://github.com/1mikegrn/libRL",
    author="Michael Green",
    author_email="michael@michaelgreen.dev",
    license="GPL-3.0",
    classifiers=[
        "Development Status :: 3 - Beta",
        "Intended Audience :: STEM research",
        "License :: OSI Approved :: GPL-3.0 License",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["scipy",],
    tests_require=["pytest", "coverage"],
    ext_modules=extensions,
    project_urls={
        "GitHub": "https://github.com/1mikegrn/libRL",
        "DocSite": "https://1mikegrn.github.io/libRL/",
        "Personal Webpage": "https://michaelgreen.dev/",
        "Google Scholar": "https://scholar.google.com/citations?user=DxFljRYAAAAJ&hl=en",
    },
)
