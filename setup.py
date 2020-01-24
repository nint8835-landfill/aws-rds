from setuptools import setup, find_packages

setup(
    name="aws-rds",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click"],
    entry_points="""
        [console_scripts]
        aws-rds=aws_rds.commands:aws_rds
    """,
)
