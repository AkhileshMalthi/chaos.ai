from setuptools import setup, find_packages

setup(
    name="chaos-ai",
    version="0.1.0",
    description="Multiplayer group storytelling game with GenAI twists",
    author="chaos.ai Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pytest>=7.4.0",
        "pytest-cov>=4.1.0",
        "pytest-mock>=3.11.0",
    ],
)
