"""
Configuration d'installation pour le projet de géolocalisation RSSI.
"""

from setuptools import setup, find_packages

# Lire le README pour la description longue
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Lire les requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rssi-geolocation",
    version="1.0.0",
    author="BELLO Soboure",
    author_email="soboure.bello@gmail.com",
    description="Système de géolocalisation basé sur les signaux RSSI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soboure.bello/Geolocalisation-Cartes-RSSI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "isort>=5.10.0",
            "pre-commit>=2.20.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ],
        "ml": [
            "mlflow>=1.28.0",
            "optuna>=3.0.0",
            "shap>=0.41.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "rssi-train=main:main",
            "rssi-dashboard=src.dashboard:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    keywords="rssi, geolocation, indoor-positioning, machine-learning, deep-learning",
    project_urls={
        "Bug Reports": "https://github.com/soboure69/Geolocalisation-Cartes-RSSI/issues",
        "Source": "https://github.com/soboure69/Geolocalisation-Cartes-RSSI",
        "Documentation": "https://soboure69.github.io/Geolocalisation-Cartes-RSSI/",
    },
)
