from setuptools import setup, find_packages

setup(
    name="kubegen",
    version="0.0.3",
    author="Razaq Kasali",
    author_email="razaqkor@gmail.com",
    description="A package to generate k8s policy file",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
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
    },
    install_requires=[
        'click==7.1.1',
        'colorama==0.4.3',
        'pyfiglet==0.8.post1',
        'PyYAML==5.3.1',
        'six==1.14.0',
        'termcolor==1.1.0'
    ]
)
