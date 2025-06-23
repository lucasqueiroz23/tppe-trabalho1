UnB - Universidade de Brasilia<br>
FCTE - Faculdade de Ciência e Tecnologia em Engenharias<br>
FGA0242 - Técnicas de Programação para Plataformas Emergentes<br>
Prof. André Lanna<br>

# Trabalho prático 1

## O algoritmo Árvore-B

| Nome | Matrícula|
| :- | :- |
| Carlos Eduardo Mota Alves | 221022248 | 
| Eduardo Belarmino Silva | 221008580 | 
| Lucas Henrique Lima de Queiroz | 190091703 |
| Pedro Sampaio | 211043745|

## Como Rodar este Projeto

Este projeto utiliza um `Makefile` para facilitar a execução de comandos como instalação de dependências, execução da aplicação e execução de testes.

### Pré-requisitos

- Python 3 instalado
- Pip instalado
- Make instalado no sistema

### Instalando Dependências

```bash
make deps
```

### Executando a Aplicação

```bash
make run
```

### Executando os teste

```bash 
make test
```

### Contratos implementados

| Inv./ Pre- / Pos-cond. | Descricao | Status |
|:---|:---|:--:|
| Invariante | Todos os nós folhas estão no mesmo nível? | :white_check_mark: |
| Invariante | Para os nós internos, as chaves estão em ordem crescente? | :white_check_mark: |
| Invariante | Para os nós folhas, todos os valores estão em ordem crescente? | :white_check_mark: |
| Pré | Chave a ser inserida não existe na árvore | :white_check_mark: |
| Pré | Chave a ser removida existe na árvore | :white_check_mark: |
| Pós | Para nó-raiz, $1 \leq numChaves \leq 2 \cdot 1$, para nós internos, $t-1 \leq numChaves \leq 2 \cdot 1$ | :white_check_mark: |
| Pós | Para nó raiz, o número de filhos é $2 \leq numFilhos \leq 2\cdot t$, para nós internos, o número de filhos é $t \leq numFilhos \leq 2\cdot t$ | :white_check_mark: |
| Pós | Para a raiz, após operação de divisão, nível da árvore aumenta em uma unidade, após operação de fusão, nível da árvore diminui em uma unidade. | :white_check_mark: |

### Referências bibliográficas

   -  ZIVIANI, Nivio. Projeto de Algoritmos: com Implementações em Pascal e C – 3ª edição revista e ampliada. 3. ed. Porto Alegre: +A Educação - Cengage Learning Brasil, 2018. E-book. p.250. ISBN 9788522126590. Disponível em: https://integrada.minhabiblioteca.com.br/reader/books/9788522126590/.
  -  ZIVIANI, Nívio. Projeto de algoritmos: com implementações em Java e C++. 3. ed. rev. e ampl. São Paulo: Pioneira Thomson Learning, 2004. Disponível em: https://integrada.minhabiblioteca.com.br/reader/books/9788522108213/pageid/0. Acesso em: 22 jun. 2025.
 
