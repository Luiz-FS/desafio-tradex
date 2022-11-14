# Problemática

 

A Tradex está precisando desenvolver uma Api Rest que possa permitir adição, deleção e edição de produtos e as suas variações de preços ao longo do tempo. Precisamos poder lançar vários produtos e relacionar estes com um outro lançamento que é o de variação de preço diário.

 

Nosso funcionário reportou que está tendo muitas dificuldades de lançar produtos e consultar os dados de preço e a imagem do produto. Desta forma precisamos fornecer uma api que possa receber essas informações de produtos e sua variação de preço diário.  Esse funcionário irá cadastrar esse produto uma vez e logo após lançar suas variações de preço diária.

 

Tabelas

 

Produtos:

 

Id: uuid v4

Nome: texto de 200 caracteres
ean: número

Imagem do produto: img

Peso: número 5

Preço mínimo: decimal

Preço máximo: decimal

 

 

Variação de preço:

Id: uuid v4

Id do produto (relacionamento um para muitos)

Data

Preço

 

Solução 1:

Criar uma solução que possibilite a criação, edição e deleção de produtos

 

Solução 2 : Criar uma solução que possibilite a criação, edição e deleção de variação de preço.

Nota:  Esta solução precisa ser capaz de permitir que seja adicionado uma variação de preço numa data específica e que essa variação do preço do produto esteja entre o valor mínimo e máximo cadastrado no produto.

 

Exemplo:

 

Produto:

1, Limpa vidro lux, 78788789989, 23.0, 50.0

2, Sabão, 453545454, 3.0, 23.0

 

Variação de preço.

1, 10/10/2022, 24.0

1, 12/10/2022, 34.00

2, 12/10/2022, 12.00

 

 

Ahhhhh. O usuário também disse que precisa ter informação de log de alteração dos dados do produto pelo usuário, assim precisamos ter como controlar o usuário que laçou a informação pois serão 3 usuários fazendo isso diariamente.

 

Entrega:

 

Para entrega precisamos ter uma documentação de como implementar o projeto.
Dump da base de dados (preferencialmente PostgreSQL)

Modelo de dados

Documentação da Api (preferencialmente em Swagger)