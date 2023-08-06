import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cremma", # Replace with your own username
    version="0.0.3",
    author="Jean-Felix Gerard",
    author_email="jfgerard@outlook.com",
    description="Cremma allows to create custom reports based on user-defined metrics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeanjean1/cremma",
    packages=setuptools.find_packages(),
    install_requires=[
      'pandas',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0'], #useful for private repos
    python_requires='>=3.6',
    scripts=['bin/deploy.py']
)

# Run tests: python setup.py test
