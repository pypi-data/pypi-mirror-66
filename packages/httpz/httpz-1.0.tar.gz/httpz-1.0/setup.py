import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="httpz",
    version="1.0",
    packages=setuptools.find_packages(),
    author="Julian Nash",
    author_email="julianjamesnash@gmail.com",
    description="HTTP Status code utils",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="http status codes",
    url="https://github.com/Julian-Nash/httpz",
    include_package_data=True,
    project_urls={
        "Bug Tracker": "https://github.com/Julian-Nash/httpz",
        "Documentation": "https://github.com/Julian-Nash/httpz",
        "Source Code": "https://github.com/Julian-Nash/httpz",
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)