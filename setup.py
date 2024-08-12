from setuptools import setup, find_packages

setup(
    name='MaroviTranslation',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'PyMuPDF>=1.23.6',
        'markdown2>=2.4.10',
        'googletrans==4.0.0-rc1',
        'grobid-client-python',
    ],
    author='Felipe Felix Arias',
    author_email='felipefelixarias@gmail.com',
    description='English-Spanish Translation of Research Papers',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    url='https://github.com/felipefelixarias/MaroviTranslation',
)
