#!/usr/bin/env pwsh

[CmdletBinding(PositionalBinding=$false)]
param(
  [switch]$noprompt,
  [string]$venv_name = ".venv"
)
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$rootPath = (Resolve-Path -LiteralPath "$scriptPath/..").Path

$argsList = @(
    "--tool-path", (Resolve-Path -LiteralPath "$rootPath/Tools/BatchPatcher").Path
    "--venv-name", $venv_name
    "--linux-package-profile", "tk"
    "--pip-requirements", (Resolve-Path -LiteralPath "$rootPath/Libraries/PyKotor/requirements.txt").Path
)
if ($noprompt) { $argsList += "--noprompt" }

if ((Get-OS) -eq "Mac") {
    Write-Host "path: '$pythonExePath'"
    $versionObject = Get-Python-Version $pythonExePath
    $pyVersion = "{0}.{1}" -f $versionObject.Major, $versionObject.Minor
    Write-Host "pyversion: $versionObject major/minor $pyVersion"
    #brew update
    #brew install python-tk@$pyVersion tcl-tk --force --overwrite  # don't use, instead install from the main install_python_venv. brew will constantly try to install other python versions.
} elseif ((Get-OS) -eq "Linux") {
    if (Test-Path -Path "/etc/os-release") {
        switch ((Get-Linux-Distro-Name)) {
            "debian" {
                sudo apt-get update
                sudo apt-get install -y tcl8.6 tk8.6 tcl8.6-dev tk8.6-dev python3-tk python3-pip
                break
            }
            "ubuntu" {
                sudo apt-get update
                sudo apt-get install -y tcl8.6 tk8.6 tcl8.6-dev tk8.6-dev python3-tk python3-pip
                break
            }
            "fedora" {
                sudo dnf install -y tk-devel tcl-devel python3-tkinter
                break
            }
            "almalinux" {
                sudo yum install -y tk-devel tcl-devel python3-tkinter
                break
            }
            "rocky" {
                sudo yum install -y tk-devel tcl-devel python3-tkinter
                break
            }
            "alpine" {
                sudo apk add --update tcl tk python3-tkinter ttf-dejavu fontconfig
                break
            }
            "arch" {
                sudo pacman -Syu --noconfirm tk tcl mpdecimal
                break
            }
            "manjaro" {
                sudo pacman -Syu --noconfirm tk tcl mpdecimal
                break
            }
            "opensuse" {
                sudo zypper install -y tk-devel tcl-devel python3-tk
                break
            }
            default {
                Write-Warning "Distribution not recognized or not supported by this script."
            }
        }
    }
}

Write-Host "Installing required packages to build the batchpatcher..."
& $pythonExePath -m pip install --upgrade pip --prefer-binary --progress-bar on
& $pythonExePath -m pip install pyinstaller --prefer-binary --progress-bar on
& $pythonExePath -m pip install -r ($rootPath + $pathSep + "Tools" + $pathSep + "BatchPatcher" + $pathSep + "requirements.txt") --prefer-binary --progress-bar on
& $pythonExePath -m pip install -r ($rootPath + $pathSep + "Libraries" + $pathSep + "PyKotor" + $pathSep + "requirements.txt") --prefer-binary --progress-bar on
& $pythonExePath -m pip install -r ($rootPath + $pathSep + "Libraries" + $pathSep + "PyKotor" + $pathSep + "recommended.txt") --prefer-binary --progress-bar on
& $pythonExePath -m pip install -r ($rootPath + $pathSep + "Libraries" + $pathSep + "PyKotorFont" + $pathSep + "requirements.txt") --prefer-binary --progress-bar on
