#Save next page from randomuser and output
output=$(python -m app.apiclient.randomuser savenextpage)
if [[ $output == *'Página'*'salva'* ]]; then
    echo $(date): $output
else
    echo $(date): "Erro na execução do módulo randomuser"
fi
