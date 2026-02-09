"""
Setup configuration for Agentic SLA Orchestrator package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="agentic-sla-orchestrator",
    version="1.0.0",
    author="Lana Baturytski",
    author_email="lanab.career@gmail.com",
    description="Governance-first AI orchestrator for customer support SLA management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/agentic-sla-orchestrator",
    project_urls={
        "Bug Tracker": "https://github.com/YOUR_USERNAME/agentic-sla-orchestrator/issues",
        "Documentation": "https://github.com/YOUR_USERNAME/agentic-sla-orchestrator/blob/main/docs/ARCHITECTURE.md",
        "Source Code": "https://github.com/YOUR_USERNAME/agentic-sla-orchestrator",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
        ],
        "dashboard": [
            "streamlit>=1.28.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sla-orchestrator=orchestrator.cli:main",
        ],
    },
    include_package_data=True,
    keywords="ai machine-learning orchestrator sla customer-support governance llm",
    zip_safe=False,
)
