#!/bin/bash

# install autodock-vina (command-line version)
wget https://vina.scripps.edu/wp-content/uploads/sites/55/2020/12/autodock_vina_1_1_2_linux_x86.tgz
tar -xvf autodock_vina_1_1_2_linux_x86.tgz
rm autodock_vina_1_1_2_linux_x86.tgz

# install gnina
wget https://github.com/gnina/gnina/releases/download/v1.1/gnina
chmod +x gnina