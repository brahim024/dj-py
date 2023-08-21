from setuptools import setup,find_packages

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    long_description_content_type="text/x-rst",
    exclude_package_data={'': ['djpay/tests/*']},
    package_dir={"": "djpay"},
    packages=find_packages(where="app"),
    url= "https://github.com/brahim024/dj-py"
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Django>=2.2',
        'requests>=2.0',
        'pytest==7.4.0'
    ]
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
)
