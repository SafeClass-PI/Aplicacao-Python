#!/bin/bash
echo ''
echo "Criando configurações de BD"
echo "Configure arquivo de configuração '.env' abaixo"
echo ''

echo ''
echo "Credenciais de acesso ao MySql Server"
read -p "Insira o ip do host: " HOST
read -p "Insira o user para inserção no banco: " USER
read -p "Insira a senha do user $USER: " SENHA
echo ''
read -p "Insira o database: " DATABASE
echo ''

cat > '.env' <<EOF
HOST_DB = '$HOST'
USER_DB = '$USER'
PASSWORD_DB = '$SENHA'
DATABASE_DB = '$DATABASE'
EOF

echo ''
echo 'As credenciais configuradas são:'
echo '--------------------------------'
cat '.env'
echo '--------------------------------'

read -p "As credenciais estão corretas? (S/N) " INICIAR_API

echo ''
if [ $INICIAR_API = 'S' ]; then 
    echo '.env Criado'
else 
    echo 'RECONFIGURE AS CREDENCIAIS...'
    ./init.sh
fi