#!usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from os import system

# Criação de argumentos de linha de comando
parser = argparse.ArgumentParser(description='Simulação de escalonador.')
# parser.add_argument('quantum', type=int, help='Janela de tempo que cada processo têm por vez para executar.')
parser.add_argument('arquivo', type=str, help='Nome do arquivo que contem as descrições dos processos.')
args = parser.parse_args()

# Variáveis usadas para colorir a saída de texto
GREEN, RED, WHITE, BLUE, YELLOW =  '\033[1;32m', '\033[91m', '\033[0m', '\33[94m', '\33[93m'

# Lê o arquivo de processos e coloca todos eles em uma lista
def ler(arq):
    processos = list()
    with open(arq) as f:
        for linha in f.readlines():
            processos.append(linha.strip('\n').split())

    for i in range(len(processos)): # Converte os números para tipos inteiros
        processos[i][1] = int(processos[i][1])
        processos[i][2] = int(processos[i][2])

    processos.sort(key = lambda x: x[1]) # Ordena os processo por ordem de chegada
    return processos

def sjf(processos, lista_execucao): # Shortest Job First
    print("{}[+]{} Utilizando Shortest Job First".format(GREEN, YELLOW))
    # print("\n{}[+]{} Execução: \n".format(GREEN, WHITE))
    rodada = 0
    processos.sort(key = lambda x: (x[2], x[1])) # Ordena a fila de processos pelo tempo de duração e depois pela chegada
    while len(processos) > 0: # Enquanto ainda houverem processos aguardando na fila
        if processos[0][1] <= rodada: # Se o primeiro processo da fila já chegou
            executa(processos[0], rodada, lista_execucao) # Exibe a execução
            print(processos)
            processos[0][2] -= 1 # Executa uma rodada do processo
            rodada += 1
            if processos[0][2] == 0: # Se o processo terminou a execução
                del processos[0]

            # Verifica se algum processo menor chegou nesse momento
            for i in range(len(processos)):
                # Se o processo em questão já chegou e é menor do que o atual
                if processos[i][1] <= rodada and processos[i][2] < processos[0][2]:
                    processos.insert(0, processos.pop(i)) # Coloca o processo no inicio da lista
                    break

        else: # Se o primeiro processo ainda não chegou
            # Procura na fila pra ver se algum processo já chegou
            for i in range(len(processos)):
                if processos[i][1] <= rodada: # Se o processo em questão já chegou
                    processos.insert(0, processos.pop(i)) # Coloca o processo no inicio da lista
                    break
            else: # Se nenhum processo pode executar nesse esse momento
                executa("wait", rodada, lista_execucao)
                print(processos)
                rodada += 1
    return

def round_robin(processos, lista_execucao):
    print("{}[+]{} Utilizando Round-Robin".format(GREEN, YELLOW))
    while True:
        try:
            quantum = int(input("{}[+]{} Digite o tamanho do quantum (janela de tempo) dedicado a cada processo por vez: ".format(GREEN, WHITE)))
            break
        except:
            print("{}[-]{}Por favor, digite somente números inteiros.".format(RED, WHITE))
    print("\n{}[+]{} Execução: \n".format(GREEN, WHITE))
    rodada = 0
    while len(processos) > 0: # Enquanto ainda houverem processos aguardando execução
        if processos[0][1] <= rodada: # Se o processo no início da fila ja chegou
            if processos[0][2] >= quantum: # Se o tamanho do quantum for menor que o nº de rodadas restantes
                executa(processos[0], rodada, lista_execucao, quantum) # Executa o processo, quantum vezes
                print(processos)
                processos[0][2] -= quantum # Retira as rodadas executadas do total
                rodada += quantum
                if processos[0][2] == 0: # Se o processo terminou a execução
                    del processos[0] # Retira ele da fila
                    continue

                elif len(processos) > 1:
                    for i in range(1, len(processos)): # Vê se outro processo já chegou e pode ser executado
                        if processos[i][1] <= rodada: # Se o processo já chegou nessa rodada
                            aux = processos.pop(i) # Salva num nome auxiliar
                            processos.append(processos.pop(0)) # Move o processo atual do início para o fim da fila
                            processos.insert(0, aux) # Insere o auxiliar no início da fila
                            break

                    # Se nenhum outro processo puder executar, continua executando o mesmo

                else: # Se o próximo processo puder executar
                    processos.append(processos.pop(0)) # Move o processo atual do início para o fim da fila

            else: # Se o tamanho do quantum é maior que o nº de rodadas restantes
                executa(processos[0], rodada, lista_execucao, processos[0][2] ) # Vai executar somente o nº de rodadas restantes
                print(processos)
                rodada += processos[0][2] # Incrementa a rodada pelo número de rodadas executadas
                del processos[0] # Elimina o processo da fila, pois ele terminou de executar
        else: # Se o processo no início da fila ainda não chegou
            executa('wait', rodada, lista_execucao)
            print(processos)
            rodada += 1
            continue

def fcfs(processos, lista_execucao):
    print("{}[+]{} Utilizando First-come, First-served".format(GREEN, YELLOW))
    print("\n{}[+]{} Execução: \n".format(GREEN, WHITE))
    # Nesse caso os processos estão ordenados por ordem de chegada
    rodada = 0
    while len(processos) > 0: # Enquanto houverem processos na fila de execução
        if processos[0][1] <= rodada: # Se o processo que está primeiro na fila, já chegou na rodada atual
            executa(processos[0], rodada, lista_execucao) # Executa uma rodada do processo
            print(processos)
            processos[0][2] -= 1 # Reduz uma rodada das rodadas restantes para a conclusão do processo
            rodada += 1  # Incrementa o nº de rodadas executadas
            if processos[0][2] == 0: # Se acabou a execução do processo em questão
                del processos[0] # Remove o processo da fila de execução
        else: # Se o processo que está em primeiro na fila, não chegou ainda
            executa('wait', rodada, lista_execucao)
            print(processos)
            rodada += 1


def executa(p, rodada, lista_execucao, quantum=1): # Mantém o quantum como 1 por padrão, para as estratégias diferentes de round_robin
    if p == 'wait':
        lista_execucao.append(['wait'])
    else:
        for i in range(quantum):
            lista_execucao.append([p[0].upper(), p[2] - (i + 1)])


def exibe(lista_execucao):
    posicao = 1 # Começa com 1 ao invés de 0, pois range(0) não gera nenhuma iteração
    while True:
        system('clear')
        print("{}[+]{} Execução: \n".format(GREEN,YELLOW))
        for i in range(posicao):
            if lista_execucao[i][0] == 'wait':
                print("{}[AGUARDA]".format(GREEN))

            elif i > 0 and lista_execucao[i - 1][0] != lista_execucao[i][0]:
                print ("{}[+] {}Processo {}:".format(GREEN, YELLOW, lista_execucao[i][0]))
                print("{}[{}]{} Restantes: {}".format(GREEN, lista_execucao[i][0], WHITE, lista_execucao[i][1]))
            else:
                print("{}[{}]{} Restantes: {}".format(GREEN, lista_execucao[i][0], WHITE, lista_execucao[i][1]))

        opt = input("\n{}[+]{} Pressione 'n' para avançar, 'b' para retroceder ou 'q' para sair: ".format(GREEN, WHITE))

        if opt == 'n' and posicao < (len(lista_execucao)):
            posicao += 1
        elif opt == 'n' and posicao == (len(lista_execucao)):
            print("\n{}[+]{} Concluído.\n".format(GREEN, WHITE))
            break
        elif opt == 'b' and posicao > 0:
            posicao -= 1

        elif opt == 'q':
            raise SystemExit


def cabecalho(processos, lista_execucao):
    modos = [fcfs, sjf, round_robin]
    while True:
        opt = input("\n{}-> Escolha o algoritmo de escalonamento a ser executado:\n\n".format(GREEN)
        + "{}[0]{} First-come, First-served\n".format(BLUE, WHITE)
        + "{}[1]{} Shortest Job First\n".format(BLUE, WHITE)
        + "{}[2]{} Round-Robin\n".format(BLUE, WHITE)
        + "{}[3]{} Sair do programa\n".format(BLUE, WHITE)
        + "\n{}[+]{} Sua opção: ".format(GREEN, WHITE))

        if opt in ['0','1','2']:
            modos[int(opt)](processos, lista_execucao)
            exibe(lista_execucao)
        elif opt == '3':
            return opt
            break
        else:
            print("\n{}[-]{} Por favor, escolha uma opção válida.\n".format(RED, WHITE))


def main(arq, out=True):
    GREEN, RED, WHITE, BLUE =  '\033[1;32m', '\033[91m', '\033[0m', '\033[94m'
    processos = ler(arq)
    lista_execucao = list()
    opt = cabecalho(processos, lista_execucao)
    if opt == '3':
        print("\n{}[-]{} Encerrando...".format(RED, WHITE))
    else:
        exibe(lista_execucao)
        main(args.arquivo)


print ("""{}
  ______               _                       _
 |  ____|             | |                     | |
 | |__   ___  ___ __ _| | ___  _ __   __ _  __| | ___  _ __
 |  __| / __|/ __/ _` | |/ _ \| '_ \ / _` |/ _` |/ _ \| '__|
 | |____\__ \ (_| (_| | | (_) | | | | (_| | (_| | (_) | |
 |______|___/\___\__,_|_|\___/|_| |_|\__,_|\__,_|\___/|_|
     """.format('\033[1;32m'))
main(args.arquivo)
