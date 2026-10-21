biblioteca = list()
emprestimos = list()

def lerInteiro(mensagem, minimo):
    while True:
        try:
            numero = int(input(mensagem))
        except ValueError as e:
            print(f"Erro: {e}")
        else:
            if numero >= minimo:
                return numero
            print(f"Informe um valor maior ou igual a {minimo}!")


def lerTexto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("Este campo nao pode ficar vazio!")


def lerMatricula():
    while True:
        matricula = input("Informe a sua matricula(4 dígitos): ").strip()
        if len(matricula) == 4 and matricula.isdigit():
            return matricula
        print("Sua matricula deve conter 4 digitos numericos")


def lerISBN(mensagem):
    while True:
        isbn = input(mensagem).strip()
        digitos = isbn.replace("-", "").replace(" ", "")
        if digitos.isdigit() and len(digitos) == 13:
            return isbn
        print("ISBN invalido! Informe um codigo com 13 digitos")


def buscarIndice(lista, codigo):
    for i in range(len(lista)):
        valor = lista[i][0]
        if isinstance(valor, str) and isinstance(codigo, str):
            isbnLista = valor.replace("-", "").replace(" ", "")
            isbnBusca = codigo.replace("-", "").replace(" ", "")
            if isbnLista == isbnBusca:
                return i
        elif valor == codigo:
            return i
    return -1


def gerarCodigoEmprestimo(emprestimos):
    codigo = 1
    for emprestimo in emprestimos:
        if emprestimo[0] >= codigo:
            codigo = emprestimo[0] + 1
    return codigo

def criarLivro(isbn):
    titulo = lerTexto("Informe o titulo do livro: ")
    autor = lerTexto("Informe o autor(a) do livro: ")
    exemplares = lerInteiro("Informe a quantidade de exemplares do livro: ", 0)
    while True:
        disponiveis = lerInteiro("Informe a quantidade de livro disponiveis para emprestimo: ", 0)
        if disponiveis <= exemplares:
            break
        print("A quantidade disponivel nao pode ser maior que o total de exemplares!")
    return [isbn, titulo, autor, exemplares, disponiveis]


def cadastrarLivro(biblioteca):
    isbn = lerISBN("Informe o ISBN do livro (13 digitos): ")
    if buscarIndice(biblioteca, isbn) != -1:
        print("Erro: ja existe um livro com esse ISBN!")
    else:
        livro = criarLivro(isbn)
        biblioteca.append(livro)
        print("Inclusao Confirmada!")

def solicitarEmprestimo(biblioteca, emprestimos):
    isbn = lerISBN("Informe o ISBN do livro que deseja emprestar (13 digitos): ")
    posicao = buscarIndice(biblioteca, isbn)

    if posicao == -1:
        print("A biblioteca nao possui esse livro!")
    elif biblioteca[posicao][4] == 0:
        print("A biblioteca nao possui esse livro disponivel atualmente para emprestimo!")
    else:
        codigo = gerarCodigoEmprestimo(emprestimos)
        matricula = lerMatricula()
        data = lerTexto("Informe a data do emprestimo: ")
        dias = lerInteiro("Informe a quantidade de dias para a devolucao: ", 1)
        print(f"Prazo de devolucao: {dias} dias")
        emprestimos.append([codigo, matricula, biblioteca[posicao][0], data, dias, False])
        biblioteca[posicao][4] -= 1
        print(f"Emprestimo realizado, codigo: {codigo}")


def mostrarEmprestimo(emprestimo):
    print(f"Codigo: {emprestimo[0]} | Matricula: {emprestimo[1]} | ISBN: {emprestimo[2]} | Data: {emprestimo[3]} | Prazo: {emprestimo[4]} dias | Devolvido: {emprestimo[5]}")


def listarLivros(biblioteca):
    if not biblioteca:
        print("Nenhum livro cadastrado.")
        return

    for livro in biblioteca:
        print(
            f"ISBN: {livro[0]} | Titulo: {livro[1]} | Autor(a): {livro[2]} "
            f"| Exemplares: {livro[3]} | Disponiveis: {livro[4]}"
        )


def listarEmprestimosAtivos(emprestimos):
    encontrouAtivo = False
    for emprestimo in emprestimos:
        if not emprestimo[5]:
            mostrarEmprestimo(emprestimo)
            encontrouAtivo = True
    if not encontrouAtivo:
        print("Nenhum emprestimo ativo.")


def devolverEmprestimo(biblioteca, emprestimos):
    codigo = lerInteiro("Informe o codigo do emprestimo: ", 1)
    posicao = buscarIndice(emprestimos, codigo)

    if posicao == -1:
        print(f"Nao existe um emprestimo registrado com o codigo {codigo}")
    elif emprestimos[posicao][5] == True:
        print("Esse emprestimo ja foi devolvido!")
    else:
        emprestimo = emprestimos[posicao]
        mostrarEmprestimo(emprestimo)
        confirma = input("Confirmar devolucao? (S/N): ").strip().upper()
        if confirma == "S":
            emprestimo[5] = True
            posicaoLivro = buscarIndice(biblioteca, emprestimo[2])
            biblioteca[posicaoLivro][4] += 1
            print("Devolucao realizada!")
        else:
            print("Devolucao cancelada.")

def exibirMenu():
    print("1 - Cadastrar Livro")
    print("2 - Solicitar Emprestimo")
    print("3 - Devolver Emprestimo")
    print("4 - Listagem De Livros")
    print("5 - Listagem De Emprestimos Ativos")
    print("6 - Sair")


def desligar():
    for i in range(3, 0, -1):
        print(f"desligando sistema em {i}")


def main():
    while True:
        exibirMenu()
        opcao = lerInteiro("Qual acao deseja realizar? : ", 1)

        if opcao == 1:
            cadastrarLivro(biblioteca)
        elif opcao == 2:
            solicitarEmprestimo(biblioteca, emprestimos)
        elif opcao == 3:
            devolverEmprestimo(biblioteca, emprestimos)
        elif opcao == 4:
            listarLivros(biblioteca)
        elif opcao == 5:
            listarEmprestimosAtivos(emprestimos)
        elif opcao == 6:
            desligar()
            break
        else:
            print("Operacao inexistente!")


if __name__ == "__main__":
    main()