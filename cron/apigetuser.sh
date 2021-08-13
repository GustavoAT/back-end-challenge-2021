#Save next page from randomuser and output
output=$(python -m app.apiclient.randomuser savenextpage);
if ['$output' == '']; then
    output='Erro na execução do módulo randomuser'
fi
echo $(date): $output
