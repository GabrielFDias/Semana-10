from abc import ABC, abstractmethod
from contextlib import closing
import sqlite3
import csv


class Estrategia(ABC):
    """
    Classe Base para as estratégias (algoritmos)

    """
    @abstractmethod
    def execute(self, dados):
        """ Método em que o algoritmo é contido.
        Implementação do algoritmo na classe filha deve
        sobreescrever este método."""
        pass

    @abstractmethod
    def parametros_necessarios(self):
        """Sobreescrever este método para que retorne uma tupla
        com a lista de parâmetros necessários.
        Exemplo:
        ('algoritmo', 'dbname', 'host', 'user', 'password')
        """
        pass

    @abstractmethod
    def nome(self):
        """Sobreescrever este método para que
        retorne o nome do algoritmo utilizado."""
        pass


class Estrategia_SQLite(Estrategia):
    def execute(self, dados):
        lista_registros = []
        db = dados['db']
        with closing(sqlite3.connect(db)) as conn:
            cursor = conn.cursor()
            # query alterada para selecionar apenas as colunas total e vendido_em
            cursor.execute("SELECT total, vendido_em FROM vendas;")
            for linha in cursor.fetchall():
                lista_registros.append(linha)
        return lista_registros

    def parametros_necessarios(self):
        return ('algoritmo', 'db')

    def nome(self):
        return 'Algoritmo SQLite'


class Estrategia_CSV(Estrategia):
    def execute(self, dados):
        lista_registros = []
        arquivo = dados['arquivo']
        with open(arquivo, newline='\n') as csvfile:
            reader = csv.DictReader(csvfile)
            for line in reader:
                # selecionando apenas as colunas total e vendido_em do dicionário
                lista_registros.append(line["total"], line["vendido_em"])
        return lista_registros

    def parametros_necessarios(self):
        return ('algoritmo', 'arquivo')

    def nome(self):
        return 'Algoritmo CSV'

class Estrategia_Texto1(Estrategia):
    def execute(self, dados):
        lista = []
        dados_arquivo = dados['arquivo']
        with open(dados_arquivo, newline='\n') as arq:
            for line in arq:
                line = line.replace("\n","")
                # pular as linhas que não devem ser lidas
                if line.startswith("Arquivo") or line.startswith("*") or line.startswith("DATA"):
                    continue

                line = line.split("       ")
                lista_registros.append((line[4].strip(), float(line[3].strip()), line[0].strip()))
        return lista

    def parametros_necessarios(self):
        return ('Algoritmo', 'Arquivo')

    def nome(self):
        return 'Algoritmo Texto 1'


class Estrategia_Texto2(Estrategia):
    def execute(self, dados):
        lista = []
        dados_arquivo = dados['arquivo']
        with open(arquivo, newline='\n') as arq:
            for line in arq:
                line = line.replace("\n","")
                # pular as linhas que não devem ser lidas
                if line.startswith("Arquivo") or line.startswith("*") or line.startswith("DATA"):
                    continue

                line = line.split("       ")
                lista.append((line[1].strip(), float(line[2].strip()), line[0].strip()))
        return lista

    def parametros_necessarios(self):
        return ('Algoritmo', 'Arquivo')

    def nome(self):
        return 'Algoritmo Texto 2'
