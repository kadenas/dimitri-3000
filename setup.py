from setuptools import setup, find_packages

setup(
    name="pysipp-gui",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pysipp",
        "PyQt6",
        "pyyaml",
        "netifaces",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "flake8",
        ]
    },
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="GUI Application for SIP Traffic Management using PySIPP",
    keywords="sip, voip, testing, pysipp, gui",
)