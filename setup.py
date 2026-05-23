"""
Setup script for AgentForge-CLI.

Provides pip-installable package with the 'agentforge' console command.
"""

from setuptools import setup, find_packages

setup(
    name="agentforge-cli",
    version="1.0.0",
    description="AI Agent engineering scaffold and compliance checking engine",
    long_description=open("README.md").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="AgentForge Team",
    license="MIT",
    url="https://github.com/agentforge/agentforge-cli",
    packages=find_packages(),
    package_data={
        "agentforge": [],
    },
    # Include templates directory
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        # Zero external dependencies -- only Python standard library
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agentforge=agentforge.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
