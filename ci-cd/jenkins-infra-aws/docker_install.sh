#!/bin/bash

# Function to print messages with color
print_message() {
    GREEN='\033[0;32m'
    NC='\033[0m' # No Color
    echo -e "${GREEN}$1${NC}"
}

# Update package database
print_message "Updating package database..."
sudo apt update
if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to update package database."
    exit 1
fi

# Upgrade existing packages
print_message "Upgrading existing packages..."
sudo apt upgrade -y
if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to upgrade existing packages."
    exit 1
fi

# Install required packages
print_message "Installing required packages..."
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to install required packages."
    exit 1
fi

# Add Docker’s official GPG key
print_message "Adding Docker’s GPG key..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to add Docker’s GPG key."
    exit 1
fi

# Add Docker APT repository
print_message "Adding Docker APT repository..."
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to add Docker APT repository."
    exit 1
fi

# Update package database with Docker packages
print_message "Updating package database with Docker packages..."
sudo apt update
if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to update package database with Docker packages."
    exit 1
fi

# Install Docker
print_message "Installing Docker..."
sudo apt install -y docker-ce
if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to install Docker."
    exit 1
fi

# Start Docker manually in the background
print_message "Starting Docker manually in the background..."
sudo dockerd > /dev/null 2>&1 &
if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to start Docker daemon."
    exit 1
fi

# Add current user to Docker group
print_message "Adding current user to Docker group..."
sudo usermod -aG docker ${USER}
if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to add current user to Docker group."
    exit 1
fi

# Add Jenkins user to Docker group (if Jenkins user exists)
print_message "Adding Jenkins user to Docker group..."
sudo usermod -aG docker jenkins
if [ $? -ne 0 ]; then
    echo "Warning: Jenkins user may not exist. Skipping adding Jenkins user to Docker group."
fi

# Apply group changes
print_message "Applying group changes..."
newgrp docker
if [ $? -ne 0 ]; then
    echo "Warning: Failed to apply group changes. You may need to log out and log back in."
fi

# Set Docker socket permissions
print_message "Setting Docker socket permissions..."
sudo chmod 666 /var/run/docker.sock
if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to set Docker socket permissions."
    exit 1
fi

# Print Docker version
print_message "Verifying Docker installation..."
docker --version
if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to verify Docker installation."
    exit 1
fi

print_message "Docker installation completed successfully!"