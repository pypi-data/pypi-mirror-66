from distutils.core import setup

setup(
    name = 'biggu_pipeline',
    packages = ['biggu_pipeline'],
    version = 'v0.0.1',
    exclude=["test"],
    description = 'Pipeline abstraction for python projects that implements IoC container',
    author = 'Eduardo Salazar',
    author_email = 'eduardosalazar89@hotmail.es',
    url = 'https://github.com/esalazarv/biggu-pipeline.git',
    download_url = 'https://github.com/esalazarv/biggu-pipeline/archive/v0.0.1.zip',
    keywords = ['biggu_pipeline', 'Pipeline', 'pipes'],
    license="MIT",
    classifiers = [
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True,
    install_requires=[],
)