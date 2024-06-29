from setuptools import find_packages, setup


def parse_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()


base_requirements = parse_requirements("requirements.txt")

extra_requirements = parse_requirements("extra-requirements.txt")

setup(
    name="Graduation-Project",
    packages=find_packages(),
    install_requires=base_requirements,
    extra_require={"extra": extra_requirements},
)
