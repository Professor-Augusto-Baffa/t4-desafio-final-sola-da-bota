#!/usr/bin/env python

"""GameAI.py: INF1771 GameAI File - Where Decisions are made."""
#############################################################
#Copyright 2020 Augusto Baffa
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#############################################################
__author__      = "Augusto Baffa"
__copyright__   = "Copyright 2020, Rio de janeiro, Brazil"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "abaffa@inf.puc-rio.br"
#############################################################

import random
from Map.Position import Position

MAX_Y = 34
MAX_X = 59

# <summary>
# Game AI Example
# </summary>
class GameAI():

    player = Position()
    state = "ready"
    dir = "north"
    score = 0
    energy = 0

    prev_action = None
    destination = None

    memory = []
    gold = []
    recent_pit = []

    dying = False # If energy < 40
    dodge = False # If is trying to dodge bullets

    # 1 significa encontrar e pegar pelo menos uma pocao azul
    # 2 significa tentar matar todos os jogadores
    # 3 significa pegar o maximo de ouros possivel
    stage = 1

    def __init__(self):
        self.memory = InstantiateMemory()

    # <summary>
    # Refresh player status
    # </summary>
    # <param name="x">player position x</param>
    # <param name="y">player position y</param>
    # <param name="dir">player direction</param>
    # <param name="state">player state</param>
    # <param name="score">player score</param>
    # <param name="energy">player energy</param>
    def SetStatus(self, x, y, dir, state, score, energy):
    
        self.player.x = x
        self.player.y = y
        self.dir = dir.lower()

        self.state = state
        self.score = score
        self.energy = energy


    # <summary>
    # Get list of observable adjacent positions
    # </summary>
    # <returns>List of observable adjacent positions</returns>
    def GetObservableAdjacentPositions(self):
        ret = []
        
        if (self.player.y > 0):
            ret.append(Position(self.player.x, self.player.y - 1))
        if (self.player.x < MAX_X):
            ret.append(Position(self.player.x + 1, self.player.y))
        if (self.player.y < MAX_Y):
            ret.append(Position(self.player.x, self.player.y + 1))
        if (self.player.x > 0):
            ret.append(Position(self.player.x - 1, self.player.y))

        return ret


    # <summary>
    # Get list of all adjacent positions (including diagonal)
    # </summary>
    # <returns>List of all adjacent positions (including diagonal)</returns>
    def GetAllAdjacentPositions(self):
    
        ret = []

        if (self.player.y > 0):
            if (self.player.x > 0):
                ret.append(Position(self.player.x - 1, self.player.y - 1))
            ret.append(Position(self.player.x, self.player.y - 1))
            if (self.player.x < MAX_X):
                ret.append(Position(self.player.x + 1, self.player.y - 1))

        if (self.player.x > 0):
            if (self.plsyer.y < MAX_Y):
                ret.append(Position(self.player.x - 1, self.player.y + 1))
            ret.append(Position(self.player.x - 1, self.player.y))

        if (self.player.x < MAX_X):
            ret.append(Position(self.player.x + 1, self.player.y))
            if (self.player.y < MAX_Y):
                ret.append(Position(self.player.x + 1, self.player.y + 1))
                
        if (self.player.y < MAX_Y):
            ret.append(Position(self.player.x, self.player.y + 1))

        return ret
    

    # <summary>
    # Get next forward position
    # </summary>
    # <returns>next forward position</returns>
    def NextPosition(self):
    
        ret = None
        
        if self.dir == "north":
            ret = Position(self.player.x, self.player.y - 1)
                
        elif self.dir == "east":
                ret = Position(self.player.x + 1, self.player.y)
                
        elif self.dir == "south":
                ret = Position(self.player.x, self.player.y + 1)
                
        elif self.dir == "west":
                ret = Position(self.player.x - 1, self.player.y)

        return ret
    

    # <summary>
    # Player position
    # </summary>
    # <returns>player position</returns>
    def GetPlayerPosition(self):
        return self.player


    # <summary>
    # Set player position
    # </summary>
    # <param name="x">x position</param>
    # <param name="y">y position</param>
    def SetPlayerPosition(self, x, y):
        self.player.x = x
        self.player.y = y

    

    # <summary>
    # Observations received
    # </summary>
    # <param name="o">list of observations</param>
    def GetObservations(self, o):
    
        # IMPLEMENTAR
        # como sua solucao vai tratar as observacoes?
        # como seu bot vai memorizar os lugares por onde passou?
        # aqui, recebe-se as observacoes dos sensores para as
        # coordenadas atuais do player


        if (o == None or len(o) == 0):
            for adj in self.GetObservableAdjacentPositions(self):
                self.memory[adj.y][adj.x].safe = True
            return
        
        for s in o:
        
            if s == "blocked":
                match (self.dir):
                    case "north":
                        if (self.prev_action == "andar"):
                            self.memory[self.player.y - 1][self.player.x].blocked = True
                        elif (self.prev_action == "andar_re"):
                            self.memory[self.player.y + 1][self.player.x].blocked = True
                    case "east":
                        if (self.prev_action == "andar"):
                            self.memory[self.player.y][self.player.x + 1].blocked = True
                        elif (self.prev_action == "andar_re"):
                            self.memory[self.player.y][self.player.x - 1].blocked = True
                    case "south":
                        if (self.prev_action == "andar"):
                            self.memory[self.player.y + 1][self.player.x].blocked = True
                        elif (self.prev_action == "andar_re"):
                            self.memory[self.player.y - 1][self.player.x].blocked = True
                    case "west":
                        if (self.prev_action == "andar"):
                            self.memory[self.player.y][self.player.x - 1].blocked = True
                        elif (self.prev_action == "andar_re"):
                            self.memory[self.player.y][self.player.x + 1].blocked = True
            
            elif s == "steps":
                pass
            
            elif s == "breeze":
                pass

            elif s == "flash":
                pass

            elif s == "blueLight":
                pass

            elif s == "redLight":
                pos_mem = self.memory[self.player.y][self.player.x]
                pos_mem.timer = 300

                if "gold" not in pos_mem.content:
                    self.gold.append(pos_mem)
                    pos_mem.content.append("gold")

            elif "damage" in s:
                attacker = s[7:]

            elif "hit" in s:
                hit = s[4:]
            
            elif s.find("enemy#") > -1:
                try:
                    steps = int(s[6:])
                except:
                    pass


    # <summary>
    # No observations received
    # </summary>
    def GetObservationsClean(self):
    
        # IMPLEMENTAR
        # como "apagar/esquecer" as observacoes?
        # devemos apagar as atuais para poder receber novas
        # se nao apagarmos, as novas se misturam com as anteriores
        pass
    

    # <summary>
    # Get Decision
    # </summary>
    # <returns>command string to new decision</returns>
    def GetDecision(self):

        # IMPLEMENTAR
        # Qual a decisão do seu bot?

        # A cada ciclo, o bot segue os passos:
        # 1- Solicita observações
        # 2- Ao receber observações:
        # 2.1 - chama "GetObservationsClean()" para apagar as anteriores
        # 2.2 - chama "GetObservations(_)" passando as novas observacoes
        # 3- chama "GetDecision()" para perguntar o que deve fazer agora
        # 4- envia decisão ao servidor
        # 5- após ação enviada, reinicia voltando ao passo 1
        
        adjacentes = self.GetObservableAdjacentPositions(self)
        safeAdjs = []
        for adj in adjacentes:
            if (self.memory[adj.y][adj.x].safe):
                safeAdjs.append(adj)

        # Se nenhuma adjacência é segura, andar pra frente pois consome menos que virar
        # Se não for possível andar para frente (borda do mapa ou bloqueio), andar para trás
        if(safeAdjs == []):
            self.prev_action = "andar"
            if (self.dir == "north"):
                if (self.player.y > 0 and not self.memory[self.player.y - 1][self.player.x].blocked):
                    return "andar"
            if (self.dir == "east"):
                if (self.player.x < MAX_X and not self.memory[self.player.y][self.player.x + 1].blocked):
                    return "andar"
            if (self.dir == "south"):
                if (self.player.y < MAX_Y and not self.memory[self.player.y + 1][self.player.x].blocked):
                    return "andar"
            if (self.dir == "west"):
                if (self.player.x > 0 and not self.memory[self.player.y][self.player.x - 1].blocked):
                    return "andar"
            self.prev_action = "andar_re"
            return "andar_re"

        


        # Exemplo de decisão aleatória:
        n = random.randint(0,7)

        if n == 0:
            return "virar_direita"
        elif n == 1:
            return "virar_esquerda"
        elif n == 2:
            return "andar"
        elif n == 3:
            return "atacar"
        elif n == 4:
            return "pegar_ouro"
        elif n == 5:
            return "pegar_anel"
        elif n == 6:
            return "pegar_powerup"
        elif n == 7:
            return "andar_re"

        return ""

def InstantiateMemory():
    listay = []

    for i in range(MAX_Y):
        listax = []

        for j in range(MAX_X):
            listax.append(MemoryPosition(j, i))
        
        listay.append(listax)
    
    return listay    

class MemoryPosition():
    def __init__(self, position):
        self.position = position
        self.content = []
        self.visited = False
        self.safe = False
        self.blocked = False
        self.timer = -1

class AStarCoord():
    def __init__(self, position, dir, destination, stepped, father):
        self.position = position
        self.dir = dir
        self.destination = destination
        self.stepped = stepped
        self.heuristic = Heuristic(position, destination)
        self.adjust = self.heuristic - abs(destination.x - position.x) + abs(destination.y - position.y)
        self.father = father
        self.children = []

def CheckNeigbours(father, can_visit, visited):
    CheckNeigbour(father, can_visit, visited, father.x + 1, father.y)
    CheckNeigbour(father, can_visit, visited, father.x - 1, father.y)
    CheckNeigbour(father, can_visit, visited, father.x, father.y + 1)
    CheckNeigbour(father, can_visit, visited, father.x, father.y - 1)

# Função que avalia se um vizinho já foi percorido e se é válido antes de adicioná-lo como filho de uma outra célula
def CheckNeigbour(father, can_visit, visited, x, y):
    if ((x, y) in can_visit and (x, y) not in visited):
        father.children.append(AStarCoord(x, y, father.destination, father.stepped + father.adjust+ 1, father))
        visited.append((x, y))

def Heuristic(position, dir, destination):
    if (dir == "north"):
        if (position.x == destination.x and position.y > destination.y):
            adjust = 0
        elif (position.y >= destination.y):
            adjust = 1
        else:
            adjust = 2
    elif (dir == "east"):
        if (position.x < destination.x and position.y == destination.y):
            adjust = 0
        elif (position.x <= destination.x):
            adjust = 1
        else:
            adjust = 2
    elif (dir == "south"):
        if (position.x == destination.x and position.y < destination.y):
            adjust = 0
        elif (position.y <= destination.y):
            adjust = 1
        else:
            adjust = 2
    elif (dir == "west"):
        if (position.x > destination.x and position.y == destination.y):
            adjust = 0
        elif (position.x >= destination.x):
            adjust = 1
        else:
            adjust = 2
    else:
        return
    
    return abs(destination.x - position.x) + abs(destination.y - position.y) + adjust

def FindPath(coord):
    path = [(coord.position.x, coord.position.y)]

    while (coord.father != None):
        coord = coord.father
        path.insert(0, (coord.position.x, coord.position.y))

    return path

def AStar(position, dir, can_visit, destination):
    visited = [(position.x, position.y)]
    
    a_star_heap = [AStarCoord(position, dir, destination, 0, None)]

    while (True):
        current_coord = a_star_heap.pop(0)

        if (current_coord.heuristic == 0):
            path = FindPath(current_coord)

            return path

        CheckNeigbours(current_coord, can_visit, visited)

        a_star_heap.extend(current_coord.children)

        a_star_heap.sort(key = lambda x : x.stepped + x.heuristic)