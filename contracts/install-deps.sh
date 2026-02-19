#!/bin/bash

# Install Foundry dependencies for Speak-Up V3

echo "Installing OpenZeppelin Contracts..."
forge install OpenZeppelin/openzeppelin-contracts --no-commit

echo "Installing OpenZeppelin Contracts Upgradeable..."
forge install OpenZeppelin/openzeppelin-contracts-upgradeable --no-commit

echo "Installing Forge-Std..."
forge install foundry-rs/forge-std --no-commit

echo "Dependencies installed successfully!"
echo "Run 'forge build' to compile contracts"
