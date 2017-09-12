#!/bin/bash

ansible-playbook app.yml -i inventories/$1 --ask-vault-pass --tags deploy
