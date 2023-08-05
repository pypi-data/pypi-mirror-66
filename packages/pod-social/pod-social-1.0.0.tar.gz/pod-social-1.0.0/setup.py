from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

version = {}
with open("pod_social/version.py") as fp:
    exec(fp.read(), version)


requires = [
    "pod-base>=1.0.3,<2"
]

setup(
    name="pod-social",
    version=version['__version__'],
    url="https://github.com/FanapSoft/pod-social-python-sdk",
    license="MIT",
    author="ReZa ZaRe",
    author_email="rz.zare@gmail.com",
    description="POD Social services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["POD", "social", "post", "pod sdk"],
    packages=find_packages(exclude=("tests", "examples")),
    install_requires=requires,
    zip_safe=False,
    classifiers=[
        "Natural Language :: Persian",
        "Natural Language :: English",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires=">=2.7",
    package_data={
        "pod_social": ["*.ini", "*.json"]
    },
    project_urls={
        "Documentation": "http://docs.pod.ir/v1.0.0.2/PODSDKs/python/6460/social-services",
        "Source": "https://github.com/FanapSoft/pod-social-python-sdk",
        "Tracker": "https://github.com/FanapSoft/pod-social-python-sdk/issues"
    }
)
