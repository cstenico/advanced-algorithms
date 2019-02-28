#stenico_camila
#8530952 camila
#8937225 henrique

import random
from collections import OrderedDict

#globals, don't touch, it's art (couldnt find anything as #define)
check_janken = {1: [0, 1, 3], 2: [0, 1, 2], 3: [0, 2, 3]}

EMPTY = 0
ROCK = 1
SCISSORS = 2
PAPER = 3

posVizinhoLinha=[-1, 1, 0, 0]
posVizinhoColuna=[0, 0, -1, +1]

class Game:
    def __init__(self, rows, columns):

        #everything will be here, to be instanced as game
        self.rows=rows
        self.columns=columns
        self.pieces=0
        self.memo=OrderedDict()
        self.board=[[0 for x in range(columns)] for y in range(rows)]
        self.solutions=[]
        self.nsolutions=0
        self.hashTable = [[[random.randint(1, 2**64-1)for i in range(4)]
                       for j in range(columns)]
                      for k in range(rows)]
        #Zobrist hash table
        #https://www.youtube.com/watch?v=QYNRvMolN20

    def readGame(self):
        for i in range(self.rows):
            row=input().split()
            for j in range(self.columns):
                self.board[i][j]=int(row[j])
                if self.board[i][j]!=EMPTY:
                    self.pieces+=1

    def printGame(self):
        for i in range(self.rows):
            for j in range(self.columns):
                print (self.board[i][j], end=' ')
            print()

    #DFS and island check as oriented na monitoria

    def DFS(self, i, j, visited):
        visited[i][j] = True

        for k in range(4): 
            iCopy = i + posVizinhoLinha[k]
            jCopy = j + posVizinhoColuna[k]
            if ((iCopy >= 0 and iCopy < self.rows) and (jCopy >= 0 and jCopy < self.columns)):
                if (not visited[iCopy][jCopy] and self.board[iCopy][jCopy]):
                    # visit neighbor
                    self.DFS(iCopy, jCopy, visited)
    
    def islandCheck(self):
        visited = [[False for j in range(self.columns)] for i in range(self.rows)] 
        islands=0
        for i in range(self.rows):
            for j in range(self.columns):
                if visited[i][j]==False and self.board[i][j]:
                    self.DFS(i, j, visited)
                    islands+=1
                if(islands > 1):
                    return False
        return True    

    def checkWin(self):
        if (self.pieces == 1):
            return True
        else :
            return False

    def calculateKey(self):
        key = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != 0:
                    key ^= self.hashTable[i][j][self.board[i][j]]
        return key

    def printSolution(self):
        hits = self.memo.popitem()[1][1]
        print(hits)
        print(self.nsolutions)
        for solution in sorted(self.solutions):
            for value in solution:
                print(str(value), end=' ')
            print()

    def play (self):
        #self.printGame()
        success = False
        state_hits = 0

        key = self.calculateKey()
        if key in self.memo:
            return self.memo[key]

        if (not self.islandCheck()):
            self.memo[key] = [False, 0]
            return self.memo[key]
            
        if self.checkWin():
            for i in range(self.rows):
                for j in range(self.columns):
                    if (self.board[i][j] != EMPTY):
                        self.solutions.append([i+1, j+1, self.board[i][j]])
                        self.nsolutions +=1 
                        self.memo[key] = [True, 1]
                        return self.memo[key]

        for i in range(self.rows):
            for j in range(self.columns):
                current = self.board[i][j]
                if (current != 0):
                    for k in range(4): 
                        iCopy = i + posVizinhoLinha[k]
                        jCopy = j + posVizinhoColuna[k]
                        if ((iCopy >= 0 and iCopy < self.rows) and (jCopy >= 0 and jCopy < self.columns)):
                            neighbor = self.board[iCopy][jCopy]
                            if (neighbor not in check_janken[current]):
                                self.board[iCopy][jCopy] = current
                                self.board[i][j] = 0
                                self.pieces -= 1
                                jump = self.play()
                                if (jump[0]):
                                    success = True
                                    state_hits += jump[1]
                                self.board[iCopy][jCopy] = neighbor
                                self.board[i][j] = current
                                self.pieces += 1
        if (not success):
            self.memo[key] = [False, 0]
        else:
            self.memo[key] = [True, state_hits]
        return self.memo[key]


def checkJanken (x1, x2):
    if ((x1!=EMPTY and x2!=EMPTY) and ((x1==SCISSORS and x2==PAPER) or (x1==PAPER and x2==ROCK) or (x1==ROCK and x2==SCISSORS))):
        return True
    else: 
        return False


def main():
    sR, sC = input().split()
    game=Game(int(sR), int(sC))
    game.readGame()
    #game.printGame()
    game.play()
    game.printSolution()

if __name__ == '__main__':
    main()

#     "I want to play a game" - Jigsaw

#    ─────▄██▀▀▀▀▀▀▀▀▀▀▀▀▀██▄─────
#    ────███───────────────███────
#    ───███─────────────────███───
#    ──███───▄▀▀▄─────▄▀▀▄───███──
#    ─████─▄▀────▀▄─▄▀────▀▄─████─
#    ─████──▄████─────████▄──█████
#    █████─██▓▓▓██───██▓▓▓██─█████
#    █████─██▓█▓██───██▓█▓██─█████
#    █████─██▓▓▓█▀─▄─▀█▓▓▓██─█████
#    ████▀──▀▀▀▀▀─▄█▄─▀▀▀▀▀──▀████
#    ███─▄▀▀▀▄────███────▄▀▀▀▄─███
#    ███──▄▀▄─█──█████──█─▄▀▄──███
#    ███─█──█─█──█████──█─█──█─███
#    ███─█─▀──█─▄█████▄─█──▀─█─███
#    ███▄─▀▀▀▀──█─▀█▀─█──▀▀▀▀─▄███
#    ████─────────────────────████
#    ─███───▀█████████████▀───████
#    ─███───────█─────█───────████
#    ─████─────█───────█─────█████
#    ───███▄──█────█────█──▄█████─
#    ─────▀█████▄▄███▄▄█████▀─────
#    ──────────█▄─────▄█──────────
#    ──────────▄█─────█▄──────────
#    ───────▄████─────████▄───────
#    ─────▄███████───███████▄─────
#    ───▄█████████████████████▄───
#    ─▄███▀───███████████───▀███▄─
#    ███▀─────███████████─────▀███
#    ▌▌▌▌▒▒───███████████───▒▒▐▐▐▐
#    ─────▒▒──███████████──▒▒─────
#    ──────▒▒─███████████─▒▒──────
#    ───────▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒───────
#    ─────────████░░█████─────────
#    ────────█████░░██████────────
#    ──────███████░░███████───────
#    ─────█████──█░░█──█████──────
#    ─────█████──████──█████──────
#    ──────████──████──████───────
#    ──────████──████──████───────
#    ──────████───██───████───────
#    ──────████───██───████───────
#    ──────████──████──████───────
#    ─██────██───████───██─────██─
#    ─██───████──████──████────██─
#    ─███████████████████████████─
#    ─██─────────████──────────██─
#    ─██─────────████──────────██─
#    ────────────████─────────────
#    ─────────────██──────────────