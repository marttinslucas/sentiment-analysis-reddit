
# Análise de sentimentos através de posts no Reddit.

## Introdução:
- Através do notebook ou script é possível verificar os sentimentos de um determinado tópico no Reddit. É possível buscar em um subreddit específico ou apenas pelo tópico. Ordenar a busca de acordo com a preferência, como relevância, data ou dia (mais opções no notebook ou no help).
- A ferramenta utilizada para que o algoritmo trabalhe em qualquer linguagem é o google translate, implementado no código, que faz a checagem de cada headline antes da análise de sentimentos pelo Vader.
- Ao final do código, são mostradas as frases mais negativas e as palavras que mais aparecem nessas frases negativas, em todo conteúdo ou nas frases positivas.
- Também é mostrado um gráfico que contem a porcentagem de posts positivos, negativos ou neutros.

## Orientação:
> Há no repositório o script .py, que nada mais é que o codigo criado no notebook otimizado para ser rodado em linha de comando.

> O algoritmo traduz para inglês os tópicos encontrados que não estejam no idioma requerido pelo Vader (inglês). Neste caso, deve se atentar ao número de buscar limites, uma vez que muitas requisições de tradução podem gerar um erro provocado por muitas requisições. (Buscando alternativas ao google translate)

## Execução:
- Para executar o notebook e consequentemente o script python, será necessário utilizar o .yml do repositório para que seja criada uma cópia do ambiente virtual utilizado no projeto.

- Para gerar a chave de acesso, id do cliente e usuário, acesse: https://old.reddit.com/prefs/apps/ e sigam as instruções para gerar as chaves de acesso necessárias para a API.

- Para clonar o ambiente através do yml file acesse: https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf
    - Necessário Conda.

## Exemplos de execução via linha de comando:

- Para acessar o help, basta digitar no terminal em que o script está: python sentiment-reddit.py -h

![](/images/help.png)

- O tópico (-t), CLIENTE_ID, SECRET_KEY e USER são `OBRIGATÓRIOS`.

![](/images/command-ex.png)

### Outputs da linha de comando de exemplo:

![](/images/output-1.png)
![](/images/output-2.png)
![](/images/output-3.png)