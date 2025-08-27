from setuptools import setup, find_packages

setup(
    name="aixplain-policy-navigator",
    version="1.0.0",
    description="Multi-Agent RAG System for Government Regulation Search using aiXplain SDK",
    author="Policy Navigator Team",
    packages=find_packages(),
    install_requires=[
        "aixplain>=0.2.27",
        "python-dotenv>=1.0.1",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "pandas>=2.0.0",
        "feedparser>=6.0.0",
        "click>=8.1.0",
        "tqdm>=4.67.1",
        "pyyaml>=6.0"
    ],
    entry_points={
        'console_scripts': [
            'policy-navigator=src.interfaces.cli:cli',
        ],
    },
    python_requires=">=3.8",
)