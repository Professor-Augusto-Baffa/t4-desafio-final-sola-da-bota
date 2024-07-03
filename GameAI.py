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
    time_left = 3000

    server_scoreboard = None

    prev_action = None
    destination = None
    path = []

    memory = []
    gold = []
    potion = []
    dest_pile = []

    dying = False # If energy < 40
    dodge = False # If is trying to dodge bullets
    alone = False # If is alone in the map IMPLEMENTAR
    saw_enemy = False # If saw enemy IMPLEMENTAR
    took_damage = False # If took damage
    enemy_blocked = False
    blocked = False # If was blocked on the last move
    
    on_gold = False # If is on gold
    on_potion = False # If is on potion

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
        if (self.player.x < MAX_X - 1):
            ret.append(Position(self.player.x + 1, self.player.y))
        if (self.player.y < MAX_Y - 1):
            ret.append(Position(self.player.x, self.player.y + 1))
        if (self.player.x > 0):
            ret.append(Position(self.player.x - 1, self.player.y))

        return ret

    # Posições válidas em uma distância de 2 de manhattan
    def Manhattan2(position):
        ret = []

        if (position.x > 0):
            ret.append(Position(position.x - 1, position.y))
            if (position.x > 1):
                ret.append(Position(position.x - 2, position.y))
        if (position.x < MAX_X):
            ret.append(Position(position.x + 1, position.y))
            if (position.x < MAX_X - 1):
                ret.append(Position(position.x + 2, position.y))
        if (position.y > 0):
            ret.append(Position(position.x, position.y - 1))
            if (position.y > 1):
                ret.append(Position(position.x, position.y - 2))
        if (position.y < MAX_Y):
            ret.append(Position(position.x, position.y + 1))
            if (position.y < MAX_Y - 1):
                ret.append(Position(position.x, position.y + 2))
        if (position.x > 0 and position.y > 0):
            ret.append(Position(position.x - 1, position.y - 1))
        if (position.x < MAX_X and position.y > 0):
            ret.append(Position(position.x + 1, position.y - 1))
        if (position.x > 0 and position.y < MAX_Y):
            ret.append(Position(position.x - 1, position.y + 1))
        if (position.x < MAX_X and position.y < MAX_Y):
            ret.append(Position(position.x + 1, position.y + 1))
        
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
    
    def NextPositionBack(self):
    
        ret = None
        
        if self.dir == "south":
            ret = Position(self.player.x, self.player.y - 1)
                
        elif self.dir == "west":
                ret = Position(self.player.x + 1, self.player.y)
                
        elif self.dir == "north":
                ret = Position(self.player.x, self.player.y + 1)
                
        elif self.dir == "east":
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

        self.on_potion = False

        adjacentes = self.GetObservableAdjacentPositions()
        
        if (self.prev_action == "andar" or self.prev_action == "andar_re"):
            # Se não houver observações, marcar todas as as adjacências que estavam como perigo como seguras
            if (len(o) == 0 or ("breeze" not in o and "flash" not in o)):
                for adj in adjacentes:
                    pos_mem = self.memory[adj.y][adj.x]
                    if (pos_mem.safe == False):
                        pos_mem.safe = True
                        pos_mem.content = []
        if (o != []):
            print(o)
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
                print("BLOCKED")
                pass

            elif s == "steps":
                print("STEPS")
                pass
            
            elif s == "breeze":
                unsafe = []
                for adj in adjacentes:
                    pos_mem = self.memory[adj.y][adj.x]
                    if (pos_mem.safe == False):
                        unsafe.append(adj)
                if (len(unsafe) == 1):
                    self.memory[unsafe[0].y][unsafe[0].x].content = ["pit"]
                    around = self.Manhattan2(unsafe[0])
                    for a in around:
                        pos_mem = self.memory[a.y][a.x]
                        if ("pit" in pos_mem.content):
                            pos_mem.content.remove("pit")
                else:
                    for adj in unsafe:
                        pos_mem = self.memory[adj.y][adj.x]
                        if ("pit" not in pos_mem.content):
                            pos_mem.content.append("pit")
                print("BREEZE")
                pass

            elif s == "flash":
                unsafe = []
                for adj in adjacentes:
                    pos_mem = self.memory[adj.y][adj.x]
                    if (pos_mem.safe == False):
                        unsafe.append(adj)
                if (len(unsafe) == 1):
                    self.memory[unsafe[0].y][unsafe[0].x].content = ["teleport"]
                    around = self.Manhattan2(unsafe[0])
                    for a in around:
                        pos_mem = self.memory[a.y][a.x]
                        if ("teleport" in pos_mem.content):
                            pos_mem.content.remove("teleport")
                else:
                    for adj in unsafe:
                        pos_mem = self.memory[adj.y][adj.x]
                        if ("teleport" not in pos_mem.content):
                            pos_mem.content.append("teleport")
                print("FLASH")
                pass

            elif s == "redLight":
                pos_mem = self.memory[self.player.y][self.player.x]
                pos_mem.timer = 0

                if "potion" not in pos_mem.content:
                    self.potion.append(pos_mem)
                    pos_mem.content = ["potion"]

                self.on_potion = True
                print("REDLIGHT")
                pass

            elif s == "blueLight":
                pos_mem = self.memory[self.player.y][self.player.x]
                pos_mem.timer = 0

                if "gold" not in pos_mem.content:
                    self.gold.append(pos_mem)
                    pos_mem.content = ["gold"]
                
                self.on_gold = True
                print("BLUELIGHT")
                pass

            elif "damage" in s:
                self.took_damage = True
                attacker = s[7:]

            elif "hit" in s:
                hit = s[4:]
            
            elif s.find("enemy#") > -1:
                self.saw_enemy = True
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
        self.took_damage = False
        self.on_gold = False
        self.on_potion = False
        self.blocked = False
        self.saw_enemy = False

        pass
    
    def UpdateTimeLeft(self):
        self.time_left -= 1

        self.UpdateTileClock()

    # Diminui 1 de cada timer > 0 
    def UpdateTileClock(self):
        for pos in self.potion:
            pos.timer -= 1
        for pos in self.gold:
            pos.timer -= 1

    # Define a posição da poção mais próxima levando em consideração heurística e timer
    # Retorna None se não conhece poções
    def closest_potion(self):
        min_time = 999
        closest = None

        for mem_pos in self.potion:
            time = mem_pos.timer - 5
            disc = Heuristic(self.player, self.dir, mem_pos.position)
            if (disc > time):
                time = disc
            if (time < min_time):
                min_time = time
                closest = mem_pos
        if (closest == None):
            return None
        heuristic = Heuristic(self.player, self.dir, closest.position)
        return (closest, closest.timer - heuristic) 
    
    def closest_gold(self):
        min_time = 999
        closest = None

        for mem_pos in self.gold:
            time = mem_pos.timer - 5
            disc = Heuristic(self.player, self.dir, mem_pos.position)
            if (disc > time):
                time = disc
            if (time < min_time):
                min_time = time
                closest = mem_pos
        if (closest == None):
            return None
        heuristic = Heuristic(self.player, self.dir, closest.position)
        return (closest, closest.timer - heuristic)  

    # Retorna movimento com base na próxima posição do path traçado, assumindo que é adjacente
    # Se andar, remove a posição do path
    def MoveInPath(self):
        prox_pos = self.path[0]
        
        if (prox_pos.x == self.player.x + 1):
            if (self.dir == "north"):
                self.prev_action = "virar_direita"
                return "virar_direita"
            if (self.dir == "south"):
                self.prev_action = "virar_esquerda"
                return "virar_esquerda"
            if (self.dir == "west"):
                if (self.player.y < MAX_Y/2):
                    self.prev_action = "virar_esquerda"
                    return "virar_esquerda"
                self.prev_action = "virar_direita"
                return "virar_direita"
            if (self.memory[prox_pos.y][prox_pos.x].safe):
                self.path.pop(0)
                self.prev_action = "andar"
                return "andar"
        if (prox_pos.x == self.player.x - 1):
            if (self.dir == "north"):
                self.prev_action = "virar_esquerda"
                return "virar_esquerda"
            if (self.dir == "south"):
                self.prev_action = "virar_direita"
                return "virar_direita"
            if (self.dir == "east"):
                if (self.player.y < MAX_Y/2):
                    self.prev_action = "virar_direita"
                    return "virar_direita"
                self.prev_action = "virar_esquerda"
                return "virar_esquerda"
            if (self.memory[prox_pos.y][prox_pos.x].safe):
                self.path.pop(0)
                self.prev_action = "andar"
                return "andar"
        if (prox_pos.y == self.player.y - 1):
            if (self.dir == "west"):
                self.prev_action = "virar_direita"
                return "virar_direita"
            if (self.dir == "east"):
                self.prev_action = "virar_esquerda"
                return "virar_esquerda"
            if (self.dir == "south"):
                if (self.player.x < MAX_X/2):
                    self.prev_action = "virar_esquerda"
                    return "virar_esquerda"
                self.prev_action = "virar_direita"
                return "virar_direita"
            if (self.memory[prox_pos.y][prox_pos.x].safe):
                self.path.pop(0)
                self.prev_action = "andar"
                return "andar"
        if (prox_pos.y == self.player.y + 1):
            if (self.dir == "west"):
                self.prev_action = "virar_esquerda"
                return "virar_esquerda"
            if (self.dir == "east"):
                self.prev_action = "virar_direita"
                return "virar_direita"
            if (self.dir == "north"):
                if (self.player.x < MAX_X/2):
                    self.prev_action = "virar_direita"
                    return "virar_direita"
                self.prev_action = "virar_esquerda"
                return "virar_esquerda"
            if (self.memory[prox_pos.y][prox_pos.x].safe):
                self.path.pop(0)
                self.prev_action = "andar"
                return "andar"
        print("UNSAFE " + str(prox_pos.x) + " " + str(prox_pos.y) + " " + str(self.destination.x) + " " + str(self.destination.y))
        self.destination = None
        return ""


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

        mem_now = self.memory[self.player.y][self.player.x]
        mem_now.visited = True

        # Se chegou ao destino, remove destino
        if (self.destination != None):
            if((self.player.x == self.destination.x and self.player.y == self.destination.y) or self.memory[self.destination.y][self.destination.x].blocked):
                self.destination = None

        if (self.energy == 0):
            return ""
        
        adjacentes = self.GetObservableAdjacentPositions()
        safeAdjs = []
        for adj in adjacentes:
            pos_mem = self.memory[adj.y][adj.x]
            if (pos_mem.safe):
                safeAdjs.append(adj)
                add = True
                for dest in self.dest_pile:
                    if (dest.x == adj.x and dest.y == adj.y):
                        add = False
                        break
                if (add):
                    if (not pos_mem.visited and not pos_mem.blocked):
                        self.dest_pile.append(adj)
        print("DEST PILE")
        for adj in self.dest_pile:
            print(adj.x, adj.y)
        print("---")
        
        # Se passar por cima do ouro, sempre pegar
        mem_now = self.memory[self.player.y][self.player.x]
        if (mem_now.content == ["gold"] and mem_now.timer <= 0):
            mem_now.timer += 150
            if (not self.dodge):
                self.prev_action = "pegar_ouro"
            self.on_gold = False
            return "pegar_ouro"
        
        # Se passar por cima da poção e não estiver com energia cheia, sempre pegar (a não ser que esteja sozinho pois não tem mais perigo)
        if (mem_now.content == ["potion"] and mem_now.timer <= 0 and not self.alone):
            mem_now.timer += 150
            if (not self.dodge):
                self.prev_action = "pegar_powerup"
            self.on_potion = False
            return "pegar_powerup"

        if (not self.dying and self.energy <= 50):
            self.dying = True
        else:
            self.dying = False
    
        
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


        # Se está em dodge, continua até terminar movimento de dodge e desliga flag
        if (self.dodge):
            if (self.prev_action == "virar_direita" or self.prev_action == "virar_esquerda"):
                self.dodge = False
                self.prev_action = "andar"
                return "andar"
            
            next_pos = Position(self.player.x + 1, self.player.y)
            for adj in safeAdjs:
                if (next_pos.x == adj.x and next_pos.y == adj.y):
                    self.prev_action = "virar_direita"
                    return "virar_direita"
            next_pos = Position(self.player.x - 1, self.player.y)
            for adj in safeAdjs:
                if (next_pos.x == adj.x and next_pos.y == adj.y):
                    self.prev_action = "virar_esquerda"
                    return "virar_esquerda"
                
            if (self.prev_action == "andar"):
                next_pos = self.NextPosition()
                for adj in safeAdjs:
                    if (next_pos.x == adj.x and next_pos.y == adj.y):
                        self.prev_action = "andar"
                        return "andar"
                self.prev_action = "andar_re"
                return "andar_re"
            if (self.prev_action == "andar_re"):
                next_pos = self.NextPositionBack()
                for adj in safeAdjs:
                    if (next_pos.x == adj.x and next_pos.y == adj.y):
                        self.prev_action = "andar_re"
                        return "andar_re"
                self.prev_action = "andar"
                return "andar"

        closest_potion = self.closest_potion()

        if (self.took_damage):
            self.took_damage = False
            # Se está morrendo ou não sabe onde tem poção, começa dodge
            if (self.dying or closest_potion == None):
                self.dest_pile.append(self.destination)
                self.destination = None
                self.path = []

                self.dodge = True

                next_pos = self.NextPosition()
                for adj in safeAdjs:
                    if (next_pos.x == adj.x and next_pos.y == adj.y):
                        self.prev_action = "andar"
                        return "andar"
                next_pos = self.NextPositionBack()
                for adj in safeAdjs:
                    if (next_pos.x == adj.x and next_pos.y == adj.y):
                        self.prev_action = "andar_re"
                        return "andar_re"
                next_pos = Position(self.player.x + 1, self.player.y)
                for adj in safeAdjs:
                    if (next_pos.x == adj.x and next_pos.y == adj.y):
                        self.prev_action = "virar_direita"
                        return "virar_direita"
                self.prev_action = "virar_esquerda"
                return "virar_esquerda"
            
            if (self.saw_enemy and not self.enemy_blocked):
                self.saw_enemy = False
                self.prev_action = "atacar"
                return "atacar"
            
            # Procura pra atirar
            self.prev_action = "virar_direita"
            return "virar_direita"

        if (self.saw_enemy and not self.enemy_blocked):
                self.prev_action = "atacar"
                return "atacar"

        if (closest_potion == None):
            print("Procurando poção")
            # Se ainda não conhece poções, procurar (se não já estiver procurando)
            if (self.destination == None or self.path == []):
                if (self.dest_pile == []):
                    adjacentes = self.GetObservableAdjacentPositions()
                    for adj in adjacentes:
                        if (self.memory[adj.y][adj.x].visited and not self.memory[adj.y][adj.x].blocked):
                            self.dest_pile.append(adj)
                self.dest_pile.sort(key = lambda x : Heuristic(self.player, self.dir, x))
                self.destination = self.dest_pile.pop(0)
                self.path = AStar(self.player, self.dir, self.destination, self.memory)
                return self.MoveInPath()
            
            # Se ainda não conhece poções, continua procurando
            if (self.destination != None):
                return self.MoveInPath()
        
        # JÁ TEM POÇÃO
        
        if (self.destination == closest_potion[0].position):
            return self.MoveInPath()

        # Se ta em cima de um spawn de poção e falta menos de 10 pra acabar, gira e espera
        if (self.player.x == closest_potion[0].position.x and self.player.y == closest_potion[0].position.y):
            print("Esperando poção")
            if closest_potion[0].timer <= 10:
                self.prev_action = "virar_direita"
                return "virar_direita"

        if (self.dying):
            self.destination = closest_potion[0].position
            self.path = AStar(self.player, self.dir, self.destination, self.memory)
            return self.MoveInPath()

        closest_gold = self.closest_gold() 

        if (closest_gold != None):
            # Se ta em cima de um spawn de ouro e falta menos de 10 pra acabar, gira e espera
            if (self.player.x == closest_gold[0].position.x and self.player.y == closest_gold[0].position.y):
                print("Esperando ouro")
                if closest_gold[0].timer <= 10:
                    self.prev_action = "virar_direita"
                    return "virar_direita"
                
            if (self.destination == closest_gold[0].position):
                return self.MoveInPath()
            
            if (closest_gold[1] < closest_potion[1]):
                if (closest_gold[1] < 5):
                    self.destination = closest_gold[0].position
                    self.path = AStar(self.player, self.dir, self.destination, self.memory)
                    return self.MoveInPath()
            if (closest_potion[1] < 5):
                    self.destination = closest_potion[0].position
                    self.path = AStar(self.player, self.dir, self.destination, self.memory)
                    return self.MoveInPath()
        else:
            if (closest_potion[1] < 5):
                self.destination = closest_potion[0].position
                self.path = AStar(self.player, self.dir, self.destination, self.memory)
                return self.MoveInPath()
            
        flag = random.randint(0, 2)
        if (self.prev_action == "virar_direita" or self.prev_action == "virar_esquerda" or flag == 0):
                prox_pos = self.NextPosition()
                if (prox_pos.x < MAX_X and prox_pos.y < MAX_Y and prox_pos.x >= 0 and prox_pos.y >= 0):
                    if (self.memory[prox_pos.y][prox_pos.x].safe):
                        self.prev_action = "andar"
                        return "andar"
                self.prev_action = "virar_direita"
                return "virar_direita"
        if (len(self.gold) >= 2 and flag == 1):
            if (self.player.x < MAX_X/2):
                sideR = 1
            else:
                sideR = 0
            if (self.player.y < MAX_Y/2):
                sideD = 1
            else:
                sideD = 0
            match (self.dir):
                case "north":
                    if (sideR == 1):
                        self.prev_action = "virar_direita"
                        return "virar_direita"
                    self.prev_action = "virar_esquerda"
                    return "virar_esquerda"
                case "east":
                    if (sideD == 1):
                        self.prev_action = "virar_direita"
                        return "virar_direita"
                    self.prev_action = "virar_esquerda"
                    return "virar_esquerda"
                case "south":
                    if (sideR == 1):
                        self.prev_action = "virar_esquerda"
                        return "virar_esquerda"
                    self.prev_action = "virar_direita"
                    return "virar_direita"
                case "west":
                    if (sideD == 1):
                        self.prev_action = "virar_esquerda"
                        return "virar_esquerda"
                    self.prev_action = "virar_direita"
                    return "virar_direita"
                
        if (self.dest_pile == []):
            adjacentes = self.GetObservableAdjacentPositions()
            for adj in adjacentes:
                if (self.memory[adj.y][adj.x].visited and not self.memory[adj.y][adj.x].blocked):
                    self.dest_pile.append(adj)
        self.dest_pile.sort(key = lambda x : Heuristic(self.player, self.dir, x))
        self.destination = self.dest_pile.pop(0)
        self.path = AStar(self.player, self.dir, self.destination, self.memory)
        return self.MoveInPath()

def InstantiateMemory():
    listay = []

    for i in range(MAX_Y):
        listax = []

        for j in range(MAX_X):
            listax.append(MemoryPosition(Position(j, i)))
        
        listay.append(listax)
    
    return listay    

class MemoryPosition():
    def __init__(self, position):
        self.position = position
        self.content = []
        self.visited = False
        self.safe = False
        self.blocked = False
        self.timer = 150

class AStarCoord():
    def __init__(self, position, dir, destination, stepped, father):
        self.position = position
        self.dir = dir
        self.destination = destination
        self.stepped = stepped
        self.heuristic = Heuristic(position, dir, destination)
        self.adjust = self.heuristic - abs(destination.x - position.x) + abs(destination.y - position.y)
        self.father = father
        self.children = []

def CheckNeighbours(father, memory, visited):
    CheckNeighbour(father, memory, visited, father.position.x + 1, father.position.y, "east")
    CheckNeighbour(father, memory, visited, father.position.x - 1, father.position.y, "west")
    CheckNeighbour(father, memory, visited, father.position.x, father.position.y + 1, "south")
    CheckNeighbour(father, memory, visited, father.position.x, father.position.y - 1, "north")

# Função que avalia se um vizinho já foi percorido e se é válido antes de adicioná-lo como filho de uma outra célula
def CheckNeighbour(father, memory, visited, x, y, dir):
    if (x < 0 or x >= MAX_X or y < 0 or y >= MAX_Y):
        return
    if ((memory[y][x].visited or (father.destination.x, father.destination.y) == (x, y)) and (x, y) not in visited):
        father.children.append(AStarCoord(Position(x, y), dir, father.destination, father.stepped + father.adjust + 1, father))
        visited.append((x, y))

def Heuristic(position, dir, destination):
    if (dir == "north"):
        if (position.x == destination.x and position.y >= destination.y):
            adjust = 0
        elif (position.y >= destination.y):
            adjust = 1
        else:
            adjust = 2
    elif (dir == "east"):
        if (position.x <= destination.x and position.y == destination.y):
            adjust = 0
        elif (position.x <= destination.x):
            adjust = 1
        else:
            adjust = 2
    elif (dir == "south"):
        if (position.x == destination.x and position.y <= destination.y):
            adjust = 0
        elif (position.y <= destination.y):
            adjust = 1
        else:
            adjust = 2
    elif (dir == "west"):
        if (position.x >= destination.x and position.y == destination.y):
            adjust = 0
        elif (position.x >= destination.x):
            adjust = 1
        else:
            adjust = 2
    else:
        return
    
    return abs(destination.x - position.x) + abs(destination.y - position.y) + adjust

def FindPath(coord):
    path = [Position(coord.position.x, coord.position.y)]

    while (coord.father != None):
        coord = coord.father
        if (coord.father == None):
            break
        path.insert(0, Position(coord.position.x, coord.position.y))

    return path

def AStar(position, dir, destination, memory):
    print("AESTRELA" + str(destination.x) + str(destination.y))
    visited = [(position.x, position.y)]
    
    a_star_heap = [AStarCoord(position, dir, destination, 0, None)]

    while (True):
        
        current_coord = a_star_heap.pop(0)
        
        if (current_coord.heuristic == 0):
            path = FindPath(current_coord)

            return path

        CheckNeighbours(current_coord, memory, visited)
        
        a_star_heap.extend(current_coord.children)
        
        a_star_heap.sort(key = lambda x : x.stepped + x.heuristic)