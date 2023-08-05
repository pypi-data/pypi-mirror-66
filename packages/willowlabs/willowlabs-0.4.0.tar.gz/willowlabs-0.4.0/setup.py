from __future__ import print_function
import os
import sys
import willowlabs
import subprocess
from setuptools import Command, find_packages, setup
from setuptools.command.build_py import build_py
from setuptools.command.install import install


def compile_grpc_protos():
    import grpc_tools.protoc
    proto_files = [os.path.join(directory, filename) for directory, _, files in os.walk("protos")
                   for filename in files if filename.endswith(".proto")]
    grpc_tools.protoc.main(["grpc_tools.protoc", "--proto_path=protos/", "--python_out=."] + proto_files)


class CompileGRPC(Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            import grpc_tools.protoc
        except ModuleNotFoundError:
            subprocess.call("pip install grpcio-tools==1.27.2", shell=True)
        proto_files = [os.path.join(directory, filename) for directory, _, files in os.walk("protos")
                       for filename in files if filename.endswith(".proto")]
        subprocess.call(f"python -m grpc_tools.protoc --proto_path=protos/ --python_out=. --grpc_python_out=. "
                        f"{' '.join(proto_files)}", shell=True)


class BuildPyCommand(build_py):
    def run(self):
        subprocess.call("pip install --upgrade pip setuptools wheel", shell=True)
        self.run_command("compile_grpc")
        super(BuildPyCommand, self).run()


class InstallCommand(install):
    def run(self):
        subprocess.call("pip install --upgrade pip setuptools", shell=True)
        self.run_command("compile_grpc")
        super(InstallCommand, self).run()


if sys.version_info < (3, 7):
    print("google-api-python-client requires python3 version >= 3.7.", file=sys.stderr)
    sys.exit(1)


install_requires = [
    "google-api-python-client>=1.7.11",
    "grpcio>=1.27.0",
    "grpcio-tools>=1.27.2",
    "PyYAML>=5.3"
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    cmdclass={"compile_grpc": CompileGRPC, "build_py": BuildPyCommand},
    name="willowlabs",
    version=willowlabs.__version__,
    author="Willow Labs AS",
    author_email="lars@willowlabs.ai",
    description="A Python package for accessing the Willow Labs APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/willowlabs/willowlabs-apis-python",
    python_requires=">=3.7.0",
    install_requires=install_requires,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP"
    ]
)
