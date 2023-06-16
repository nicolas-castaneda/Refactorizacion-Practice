import csv

# Clase Vote representa una votación individual en la elección
class Vote:
    def __init__(self, row):
        self.region = row[0]
        self.province = row[1]
        self.district = row[2]
        self.dni = row[3]
        self.candidate = row[4]
        self.is_valid = row[5] == '1' and len(row[3]) == 8

# Clase Candidate representa un candidato en la elección
class Candidate:
    def __init__(self, name, first_appearance):
        self.name = name
        self.votes = 0
        self.first_appearance = first_appearance

# Clase ElectionResultsProcessor procesa los resultados de la elección.
class ElectionResultsProcessor:
    def __init__(self):
        self.candidates = {}

    def process_votes(self, data_source):
        # Procesa los votos en base a una fuente de datos
        if type(data_source) == str:
            self._process_votes_from_csv(data_source)
        elif type(data_source) == list:
            self._process_votes_from_list(data_source)
        else:
            raise ValueError("La fuente de datos no es válida")
        return self._get_winners()

    def _process_votes_from_csv(self, file_name):
        # Procesa votos desde un archivo CSV
        with open(file_name, 'r') as csvfile:
            next(csvfile)
            data_reader = csv.reader(csvfile)
            for i, row in enumerate(data_reader):
                self._process_vote(Vote(row), i)

    def _process_votes_from_list(self, data):
        # Procesa los votos desde una lista
        for i, row in enumerate(data):
            self._process_vote(Vote(row), i)

    def _process_vote(self, vote, index):
        # Procesa un voto individual
        # En caso sea válido el voto y el candidato no esté en el diccionario de candidatos, añade el candidato al diccionario
        # Independientemente de que el candidato esté en el diccionario o no, incrementa los votos del candidato
        if vote.is_valid:
            if vote.candidate not in self.candidates:
                self.candidates[vote.candidate] = Candidate(vote.candidate, index)
            self.candidates[vote.candidate].votes += 1

    def _get_winners(self):
        # Calcula el total de votos y ordena los candidatos por votos de mayor a menor
        total_votes = sum(candidate.votes for candidate in self.candidates.values())
        candidates_sorted_by_votes = sorted(self.candidates.values(), key=lambda x: x.votes, reverse=True)

        # Si el primer candidato tiene más del 50% de los votos, retorna un array con el nombre del candidato
        if candidates_sorted_by_votes[0].votes / total_votes > 0.5:
            return [candidates_sorted_by_votes[0].name]
        # Si hay un empate entre dos candidatos con 50% de votos, retorna un array con el nombre del candidato que apareció primero en el archivo
        elif candidates_sorted_by_votes[0].votes / total_votes == candidates_sorted_by_votes[1].votes / total_votes == 0.5:
            tied_candidates = [candidates_sorted_by_votes[0], candidates_sorted_by_votes[1]]
            return [min(tied_candidates, key=lambda x: x.first_appearance).name]
        # Si no hay un candidato con más del 50% de los votos, retorna un array con los dos candidatos que pasan a segunda vuelta
        else:
            return [candidate.name for candidate in candidates_sorted_by_votes[:2]]

# Instancia de ElectionResultsProcessor
election_processor = ElectionResultsProcessor()
# Procesa los votos desde un archivo CSV
winners = election_processor.process_votes('0204.csv')
# Imprime los ganadores
print(winners)

"""
    Refactorización de código:
        Extracción de métodos: 
            - Se reduce la complejidad del método process_votes al distribuir la lógica de procesamiento de votos en métodos nuevos basados en la fuente de la data llamados _process_votes_from_csv y _process_votes_from_list. Asimismo, _get_winners permite obtener los ganadores de la elección.  
        Renombrar variables y métodos: 
            - Se renombra el metodo leerdatos a process_votes y calcularganador, a _get_winners.
        Eliminar código duplicado: 
            - Se elimina código duplicado en el procesamiento de los datos tanto desde un CSV como desde una lista a través del método _process_vote que puede manejar una votación individual independientemente de la fuente de datos.
        Extracción de clases: 
            - Se añaden las clases Vote y Candidate, los cuales manejan la lógica relacionada a los votos y los candidatos, de modo que el uso de sus atributos haga más legible el código resultante.
        Simplificación de condicionales: 
            - Se analiza la condición de que un voto sea válido a través de una sola sentencia que verifica los campos de DNI y esvalido.
        Mejorar legibilidad del código y comentarios
            - Se reorganizó el código para que sea más legible y se agregaron comentarios de forma explícita e implícita a través de nombres de métodos descriptivos.
"""