from setuptools import setup, find_packages

setup(
    name="kubegen",
    version="0.0.2",
    author="Razaq Kasali",
    author_email="razaqkor@gmail.com",
    description="A package to generate k8s policy file",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'kubegen = kubegen.__main__:main'
        ]
    }
)