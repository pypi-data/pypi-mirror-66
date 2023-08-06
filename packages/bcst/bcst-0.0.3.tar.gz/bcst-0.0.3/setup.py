import setuptools

with open("README.md", "r") as readme:
        long_description = readme.read()

setuptools.setup(
        name="bcst",
        version="0.0.3",
        scripts=["bcst/bcst"],
        author="Loic Guegan",
        author_email="manzerbredes@mailbox.org",
        description="A web browser start page generator.",
        long_description=long_description,
        long_description_content_type='text/markdown',
        url="https://gitlab.com/manzerbredes/bcst",
        install_requires=["jinja2"],
        include_package_data=True,
        packages=setuptools.find_packages(),
        classifiers=["License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"])
    
