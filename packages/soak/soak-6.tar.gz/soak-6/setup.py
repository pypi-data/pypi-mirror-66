import setuptools

def long_description():
    with open('README.md') as f:
        return f.read()

setuptools.setup(
        name = 'soak',
        version = '6',
        description = 'Process aridity templates en masse, with secrets decryption',
        long_description = long_description(),
        long_description_content_type = 'text/markdown',
        url = 'https://github.com/combatopera/soak',
        author = 'Andrzej Cichocki',
        packages = setuptools.find_packages(),
        py_modules = [],
        install_requires = ['aridity', 'diapyr', 'lagoon', 'PyYAML', 'splut'],
        package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt']},
        scripts = [],
        entry_points = {'console_scripts': ['soak=soak.soak:main_soak']})
