#!/bin/bash

if command -v pwsh > /dev/null 2>&1; then
    echo "PowerShell already installed, nothing to do."
    pwsh --version
    exit 0
fi

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux installation
    echo "Installing PowerShell on Linux..."
    
    # Check if we're on Ubuntu/Debian
    if command -v apt-get &> /dev/null; then
        # Update package list
        sudo apt-get update -qq
        
        # Install dependencies
        sudo apt-get install -y -qq wget apt-transport-https software-properties-common
        
        # Download Microsoft signing key
        # Try to get Ubuntu version, fallback to 22.04 if lsb_release is not available
        if command -v lsb_release &> /dev/null; then
            UBUNTU_VERSION=$(lsb_release -rs)
        else
            # Fallback: try to detect from /etc/os-release
            if [ -f /etc/os-release ]; then
                UBUNTU_VERSION=$(grep VERSION_ID /etc/os-release | cut -d'"' -f2 | cut -d'.' -f1,2)
            else
                # Default to 22.04 if we can't detect
                UBUNTU_VERSION="22.04"
            fi
        fi
        
        wget -q "https://packages.microsoft.com/config/ubuntu/${UBUNTU_VERSION}/packages-microsoft-prod.deb" -O packages-microsoft-prod.deb || {
            echo "Warning: Failed to download packages-microsoft-prod.deb for Ubuntu ${UBUNTU_VERSION}, trying 22.04..."
            wget -q "https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb" -O packages-microsoft-prod.deb
        }
        sudo dpkg -i packages-microsoft-prod.deb
        rm packages-microsoft-prod.deb
        
        # Update package list again
        sudo apt-get update -qq
        
        # Install PowerShell
        sudo apt-get install -y -qq powershell
        
    # Check if we're on RHEL/CentOS/Fedora
    elif command -v yum &> /dev/null || command -v dnf &> /dev/null; then
        # For RHEL/CentOS/Fedora
        if command -v dnf &> /dev/null; then
            PKG_MGR=dnf
        else
            PKG_MGR=yum
        fi
        
        # Register Microsoft repository
        sudo $PKG_MGR install -y -q https://packages.microsoft.com/config/rhel/7/packages-microsoft-prod.rpm
        
        # Install PowerShell
        sudo $PKG_MGR install -y -q powershell
        
    else
        echo "Unsupported Linux distribution. Attempting generic installation..."
        # Fallback: try to install via snap or download binary
        if command -v snap &> /dev/null; then
            sudo snap install powershell --classic
        fi
    fi
    if ! command -v pwsh > /dev/null; then
        if command -v yum > /dev/null; then
            echo "Found 'yum' command"
            sudo yum update
            sudo yum install -y powershell
        fi
    fi
    if ! command -v pwsh > /dev/null; then
        if command -v zypper > /dev/null; then
            echo "Found 'zypper' command"
            sudo zypper install -y https://packages.microsoft.com/config/sles/15/packages-microsoft-prod.rpm
            sudo zypper refresh
            sudo zypper install -y powershell
        fi
    fi
    if ! command -v pwsh > /dev/null; then
        if command -v brew > /dev/null; then
            echo "Found 'brew' command"
            install_powershell_brew
        fi
    fi
    if ! command -v pwsh > /dev/null; then
        if command -v pacman > /dev/null; then
            install_powershell_archlinux
        fi
    fi
    if ! command -v pwsh > /dev/null; then
        if command -v flatpak > /dev/null; then
            echo "Installing PowerShell via Flatpak..."
            flatpak install flathub com.microsoft.powershell -y
        fi
    fi

    if command -v pwsh > /dev/null; then
        echo "PowerShell installation was successful."
    else
        echo "PowerShell installation failed."
        exit 1
    fi
}

install_powershell_archlinux() {
    sudo pacman-key --init
    sudo pacman-key --populate archlinux
    sudo pacman -Syu archlinux-keyring --noconfirm
    sudo pacman -Syy --noconfirm
    # Find the exact name of the package (if available in official repos)
    # It's more efficient to install from official repos if available
    sudo pacman -S --needed --noconfirm powershell-bin || {

        # If the package isn't found in the official repositories, proceed with AUR
        sudo pacman -S --needed --noconfirm git base-devel

        # Clone the AUR repository for powershell-bin
        git clone https://aur.archlinux.org/powershell-bin.git
        cd powershell-bin

        # Inspect the PKGBUILD - always good practice
        cat PKGBUILD

        if [ "$(id -u)" -eq 0 ]; then
            echo "This script should not be run as root, using a temporary user named 'tempuser'..."
            TEMP_USER="tempuser"  # makepkg cannot be run as root
            TEMP_PASSWORD="temppassword"
            TEMP_ENTRY='tempuser ALL=(ALL:ALL) NOPASSWD:ALL'
            # Check if tempuser exists, create if not
            if ! id "$TEMP_USER" &>/dev/null; then
                if command -v adduser > /dev/null; then
                    sudo adduser --disabled-password --gecos "" $TEMP_USER
                else
                    sudo useradd -M --no-create-home $TEMP_USER
                    #useradd -m -c "" "$new_username"
                    #echo "$TEMP_USER:$TEMP_PASSWORD" | sudo chpasswd
                fi
            fi
            # Check if the entry already exists, and if not, append it to the sudoers file
            if ! grep -P "^${TEMP_ENTRY}" /etc/sudoers; then
                echo "$TEMP_ENTRY" | sudo EDITOR='tee -a' visudo >/dev/null
                echo "Entry added successfully."
            else
                echo "Entry already exists."
            fi

            # Change ownership to tempuser for the build directory
            sudo chown -R "$TEMP_USER:$TEMP_USER" "../powershell-bin"

            echo If you are prompted to enter a password at this point, enter temppassword
            # Attempt to build the package as tempuser
            if ! echo "$TEMP_PASSWORD" | sudo -S -u "$TEMP_USER" makepkg -si --noconfirm; then
                # If makepkg fails, reset the ownership to root before exiting
                sudo chown -R root:root "../powershell-bin"
                exit 1
            fi
            # Remove the specific sudoers entry
            sudo sed -i "/^${TEMP_ENTRY}$/d" /etc/sudoers

            # Validate that the sudoers file is still OK (important!)
            sudo visudo -c

            if [ $? -eq 0 ]; then
                echo "Entry removed successfully and sudoers file is valid."
            else
                echo "An error occurred. The sudoers file may be invalid. Restoring from backup."
                sudo cp /etc/sudoers.bak /etc/sudoers
            fi

            # Reset ownership after successful build
            sudo chown -R root:root "../powershell-bin"

            # Remove the temporary user
            if command -v userdel > /dev/null; then
                sudo userdel -r "$TEMP_USER" 2>/dev/null || true
            elif command -v deluser > /dev/null; then
                sudo deluser --remove-home "$TEMP_USER" 2>/dev/null || true
            else
                echo "User deletion command not found!"
            fi
        else
            echo "ERROR: Cannot install PowerShell on this Linux distribution automatically"
            exit 1
        fi
        ;;
    *)
        echo "Unsupported operating system."
        exit 1
        ;;
esac
