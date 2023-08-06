from setuptools import find_packages, setup


if __name__ == "__main__":

    with open("README.md") as f:
        readme = f.read().strip()

    with open("HISTORY.md") as f:
        history = f.read().strip()

    with open("requirements.txt") as f:
        required_packages = f.readlines()

    keywords = []

    setup(
        packages=find_packages(),
        install_requires=required_packages,
        name="researchflow",
        version="0.0.0",
        description="TensorFlow wrapper and tools for ML research",
        long_description=f"{readme}\n\n{history}",
        long_description_content_type="text/markdown",
        license="MIT",
        author="Daniel Watson",
        author_email="daniel.watson@nyu.edu",
        keywords=keywords,
        url="https://github.com/danielwatson6/researchflow",
        # download_url="https://pypi.org/project/elastictools/",
    )
