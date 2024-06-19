#!/usr/bin/python3

from pathlib import Path
import platform
import shutil
from subprocess import call
import sys

from constants.randoconstants import VERSION

base_name = f"Skyward Sword HD Randomizer {VERSION}"

compile_command = [
    sys.executable,  # Uses the same python install as is currently being used to run build.py
    "-m",
    "nuitka",
]

exe_ext = ""

if platform.system() == "Windows":
    exe_ext = ".exe"
    platform_name = "windows"
    compile_command += [
        "--onefile",
        "--windows-console-mode=disable",
        "--windows-icon-from-ico=assets/icon.png",
    ]
if platform.system() == "Darwin":
    exe_ext = ".app"
    platform_name = "macos"
    compile_command += [
        "--macos-create-app-bundle",
        "--macos-app-icon=assets/icon.png",
        f"--macos-app-name={base_name}",
        f"--macos-app-version={VERSION}",
    ]
if platform.system() == "Linux":
    platform_name = "linux"
    compile_command += [
        "--onefile",
        "--linux-icon=assets/icon.png",
    ]

compile_command += [
    "--enable-plugin=pyside6",
    "--enable-plugin=multiprocessing",
    "--include-data-files=asm/additions/diffs/*.yaml=asm/additions/diffs/",
    "--include-data-files=asm/patches/diffs/*.yaml=asm/patches/diffs/",
    "--include-data-files=sshd_extract/README.md=sshd_extract/",
    "--include-data-files=*.md=./",
    "--include-data-files=LICENSE=./",
    "--include-data-dir=assets=assets",
    "--include-data-dir=data=data",
    "--include-data-dir=gui/custom_themes=gui/custom_themes",
    "--include-data-dir=plandomizers=plandomizers",
    "--include-data-dir=presets=presets",
    f"--output-filename={base_name}",
    "--output-dir=dist",
    "--remove-output",
    "sshdrando.py",
]

if result := call(compile_command):
    raise Exception(f"Nuitka failed to compile the randomizer: {result}")

macos_default_build_path = Path("dist") / "sshdrando.app"
if macos_default_build_path.exists():
    shutil.move(macos_default_build_path, Path("dist") / (base_name + exe_ext))

exe_path = Path("dist") / (base_name + exe_ext)

if not exe_path.is_file() and not exe_path.is_dir():
    raise Exception(f"Executable not found: {exe_path}")

# Give non-windows builds execute permissions
if platform.system() != "Windows":
    exe_path.chmod(0o755)

release_archive_path = Path("dist") / f"release_archive_{VERSION}_{platform_name}"
print(f"Writing build to path: {release_archive_path}")

if release_archive_path.exists() and release_archive_path.is_dir():
    shutil.rmtree(release_archive_path)

release_archive_path.mkdir(exist_ok=True)
shutil.copyfile("README.md", release_archive_path / "README.txt")

shutil.copytree(
    Path("plandomizers") / "examples",
    release_archive_path / "plandomizers" / "examples",
)
shutil.copyfile(
    Path("plandomizers") / "vanilla_boko_base.yaml",
    release_archive_path / "plandomizers" / "vanilla_boko_base.yaml",
)

(release_archive_path / "presets").mkdir(exist_ok=True)
shutil.copyfile(
    Path("presets") / "README.md", release_archive_path / "presets" / "README.txt"
)

(release_archive_path / "sshd_extract").mkdir(exist_ok=True)
shutil.copyfile(
    Path("sshd_extract") / "README.md",
    release_archive_path / "sshd_extract" / "README.txt",
)

shutil.move(exe_path, release_archive_path / (base_name + exe_ext))
