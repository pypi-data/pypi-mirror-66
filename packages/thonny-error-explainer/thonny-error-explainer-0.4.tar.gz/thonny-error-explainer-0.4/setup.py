import setuptools
import os.path

setupdir = os.path.dirname(__file__)

with open("README.md", "r") as rm:
    long_description = rm.read()

requirements = []
for line in open(os.path.join(setupdir, "requirements.txt"), encoding="UTF-8"):
    if line.strip() and not line.startswith("#"):
        requirements.append(line)

setuptools.setup(
    name="thonny-error-explainer",
    version="0.4",
    description="Thonny plugin for error-explainer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kaarel Loide",
    author_email="kaarel.loide@gmail.com",
    url="https://github.com/K44rel/thonny-error-explainer-plugin",
    packages=["thonnycontrib.error-explainer"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=requirements,
)