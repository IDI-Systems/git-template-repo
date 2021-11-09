import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="git-template-repo",
    version="0.5.0",
    author="IDI-Systems",
    author_email="contact@idi-systems.com",
    description="A git command for creating a git repo from another repo as a template.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idi-systems/git-template-repo",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['git-template-repo=git_template_repo:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
