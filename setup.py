from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="Al-Faraheedy-Python",
    version="1.0.0",
    author="Muktar Sayed Saleh",
    author_email="muktar@monjz.com",
    description="Al Faraheedy Python, A Pythonized version of the Arabic Poetry Rhythm and Rhyme Analyzer Project - مكتبة بايثون تغلّف نظام الفراهيدي لحوسبة عروض الشعر العربي و قافيته",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muktarsayedsaleh/al-faraheedy-python",
    project_urls={
        "Bug Tracker": "https://github.com/muktarsayedsaleh/al-faraheedy-python/issues",
        "Documentation": "https://al-faraheedy.readthedocs.io/",
        "Source Code": "https://github.com/muktarsayedsaleh/al-faraheedy-python",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Natural Language :: Arabic",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "isort>=5.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "faraheedy=al_faraheedy.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "al_faraheedy": ["data/*.json", "data/*.txt"],
    },
    keywords=[
        "arabic", "poetry", "prosody", "nlp", "linguistics", "meter", "rhyme",
        "عربي", "شعر", "عروض", "قافية", "بحر"
    ],
    zip_safe=False,
)