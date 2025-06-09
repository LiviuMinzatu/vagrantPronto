#!/bin/bash

echo "Avvio diagnostica sistema..."
sleep 1

# Controlla se neofetch è installato
if ! command -v neofetch &> /dev/null; then
    echo "neofetch non trovato. Installazione in corso..."
    OS="$(uname -s)"

    if [[ "$OS" == "Darwin" ]]; then
        if ! command -v brew &> /dev/null; then
            echo "Homebrew non installato. Installalo prima da https://brew.sh"
            exit 1
        fi
        brew install neofetch
    elif [[ "$OS" == "Linux" ]]; then
        if [ -f /etc/debian_version ]; then
            sudo apt update
            sudo apt install -y neofetch
        elif [ -f /etc/redhat-release ]; then
            sudo dnf install -y neofetch
        else
            echo "Distribuzione non supportata per neofetch"
        fi
    fi
fi

# Esegui neofetch
neofetch
sleep 3

echo "Verifica sistema operativo..."
OS="$(uname -s)"

install_vagrant=false
install_ansible=false

# Verifica Vagrant
if ! command -v vagrant &> /dev/null; then
    echo "Vagrant non trovato."
    install_vagrant=true
else
    echo "Vagrant è installato: $(vagrant --version)"
fi

# Verifica Ansible
if ! command -v ansible &> /dev/null; then
    echo "Ansible non trovato."
    install_ansible=true
else
    echo "Ansible è installato: $(ansible --version | head -n 1)"
fi

# Installazioni
if [[ "$OS" == "Darwin" ]]; then
    echo "Sistema operativo: macOS"
    if ! command -v brew &> /dev/null; then
        echo "Homebrew non installato. Installalo prima: https://brew.sh"
        exit 1
    fi

    if $install_vagrant; then
        echo "Installazione di Vagrant..."
        brew install --cask vagrant
    fi

    if $install_ansible; then
        echo "Installazione di Ansible..."
        brew install ansible
    fi

elif [[ "$OS" == "Linux" ]]; then
    echo "Sistema operativo: Linux"

    if [ -f /etc/debian_version ]; then
        PKG_MANAGER="apt"
        SUDO="sudo"
    elif [ -f /etc/redhat-release ]; then
        PKG_MANAGER="dnf"
        SUDO="sudo"
    else
        echo "Distribuzione non supportata"
        exit 1
    fi

    if $install_vagrant; then
        echo "Installazione di Vagrant..."
        $SUDO $PKG_MANAGER update -y
        $SUDO $PKG_MANAGER install -y vagrant
    fi

    if $install_ansible; then
        echo "Installazione di Ansible..."
        $SUDO $PKG_MANAGER install -y ansible
    fi

else
    echo "Sistema operativo non riconosciuto: $OS"
    exit 1
fi

echo "Setup completato."

