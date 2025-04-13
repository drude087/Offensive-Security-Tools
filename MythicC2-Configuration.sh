#!/bin/bash

# Update and upgrade the system
echo "----------UPDATING THE SYSTEM----------"
sudo apt update && sudo apt upgrade -y

# Create a directory and clone the Mythic repository
mkdir access
cd access
echo "----------CLONING MYTHIC C2----------"
git clone https://github.com/its-a-feature/Mythic.git
cd Mythic

# Install Docker and other dependencies
echo "----------INSTALLING THE KALI VERSION----------"
sudo ./install_docker_kali.sh

# Build the Mythic CLI binary
echo "----------BUILDING THE MYTHIC CLI BINARY----------"
sudo make

# Install Athena agent
echo "----------INSTALLING THE AGENT ATHENA----------"
sudo -E ./mythic-cli install github https://github.com/MythicAgents/Athena.git

# Install HTTP C2 profile
echo "----------INSTALLING THE PROFILE----------"
sudo ./mythic-cli install github https://github.com/MythicC2Profiles/http

# To get the credentials
echo "----------SAVING THE CREDENTIALS----------"
cat .env | grep "MYTHIC_ADMIN_USER\|MYTHIC_ADMIN_PASSWORD" > credentials.txt

# If you go to the Mythic folder you will find the credentials

# Start Mythic
echo "----------STARTING MYTHIC C2 THIS MIGHT TAKE SOME TIME----------"
sudo ./mythic-cli start

echo "----------TO STOP IT GO TO THE MYTHIC FOLDER AND RUN sudo ./mythic-cli stop----------"
