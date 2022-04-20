
from Agent import Agent
from Actions import Actions
from AgentAI import AgentAI
import random
import numpy as np

class Grid():
    
    # Tile Structure
    class __Tile:
        pit    = False;
        wumpus = False;
        gold   = False;
        breeze = False;
        stench = False;

    
    def __init__ ( self, debug = False, randomAI = False, file = None ):
        # Operation Flags
        self.__debug        = debug
        
        # Agent Initialization
        self.__goldLooted   = False
        self.__hasArrow     = True
        self.__bump         = False
        self.__scream       = False
        self.__score        = 0
        self.__agentDir     = 0
        self.__agentX       = 0
        self.__agentY       = 0
        self.__lastAction   = Agent.Action.CLIMB
        
        if randomAI:
            self.__agent = Actions()

        else:
            self.__agent = AgentAI()
            
        if file != None:
            self.__colDimension, self.__rowDimension = [int(x) for x in next(file).split()]
            self.__board = [[self.__Tile() for j in range(self.__rowDimension)] for i in range(self.__colDimension)]
            self.__addFeatures(file)
        else:
            self.__colDimension = 5
            self.__rowDimension = 5
            self.__board = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)]
            self.__addFeatures()
    

    
    def run ( self ):
        while self.__score >= -1000:
            if self.__debug:
                self.__printGridInfo()
                ax=1
                if ax==1:
                    input("\n\t \t \t \t \t \t \t Press ENTER for next step...\n")
                        
            # Get the move
            self.__lastAction = self.__agent.getAction (
														self.__board[self.__agentX][self.__agentY].stench,
														self.__board[self.__agentX][self.__agentY].breeze,
														self.__board[self.__agentX][self.__agentY].gold,
														self.__bump,
														self.__scream
													   )

            # Make the move
            self.__score -= 1;
            self.__bump   = False;
            self.__scream = False;
            
            if self.__lastAction == Agent.Action.TURN_LEFT:
                self.__agentDir -= 1
                if (self.__agentDir < 0):
                    self.__agentDir = 3
                    
            elif self.__lastAction == Agent.Action.TURN_RIGHT:
                self.__agentDir += 1
                if self.__agentDir > 3:
                    self.__agentDir = 0
                    
            elif self.__lastAction == Agent.Action.FORWARD:
                if self.__agentDir == 0 and self.__agentX+1 < self.__colDimension:
                    self.__agentX += 1
                elif self.__agentDir == 1 and self.__agentY-1 >= 0:
                    self.__agentY -= 1
                elif self.__agentDir == 2 and self.__agentX-1 >= 0:
                    self.__agentX -= 1
                elif self.__agentDir == 3 and self.__agentY+1 < self.__rowDimension:
                    self.__agentY += 1
                else:
                    self.__bump = True
                    
                if self.__board[self.__agentX][self.__agentY].pit or self.__board[self.__agentX][self.__agentY].wumpus:
                    self.__score -= 1000
                    if self.__debug:
                        self.__printGridInfo()
                    return self.__score
                
            elif self.__lastAction == Agent.Action.SHOOT:
            
                if self.__hasArrow:
                    self.__hasArrow = False
                    self.__score -= 10
                    
                    if self.__agentDir == 0:
                        for x in range (self.__agentX, self.__colDimension):
                                if self.__board[x][self.__agentY].wumpus:
                                    self.__board[x][self.__agentY].wumpus = False
                                    self.__board[x][self.__agentY].stench = True
                                    self.__scream = True
                    
                    elif self.__agentDir == 1:
                        for y in range (self.__agentY, -1, -1):
                            if self.__board[self.__agentX][y].wumpus:
                                self.__board[self.__agentX][y].wumpus = False
                                self.__board[self.__agentX][y].stench = True
                                self.__scream = True
                    
                    elif self.__agentDir == 2:
                        for x in range (self.__agentX, -1, -1):
                            if self.__board[x][self.__agentY].wumpus:
                                self.__board[x][self.__agentY].wumpus = False
                                self.__board[x][self.__agentY].stench = True
                                self.__scream = True

                    elif self.__agentDir == 3:
                        for y in range (self.__agentY, self.__rowDimension):
                            if self.__board[self.__agentX][y].wumpus:
                                self.__board[self.__agentX][y].wumpus = False
                                self.__board[self.__agentX][y].stench = True
                                self.__scream = True
                    
            elif self.__lastAction == Agent.Action.GRAB:
                if self.__board[self.__agentX][self.__agentY].gold:
                    self.__board[self.__agentX][self.__agentY].gold = False
                    self.__goldLooted = True
                    
            elif self.__lastAction == Agent.Action.CLIMB:
                if self.__agentX == 0 and self.__agentY == 0:
                    if self.__goldLooted:
                        self.__score += 1000
                    if (self.__debug):
                        self.__printGridInfo()
                    return self.__score;
        return self.__score
        
    
    def __addFeatures ( self, file = None ):
        if file == None:
            import random
            
            colNum = random.sample(range(0, 5), 5)
            rowNum = random.sample(range(0, 5), 5)
            Co = [[3,1,2,4,0,3,1],[1,2,4,3,0,2,0],[1,3,4,0,2,1,1],[1,3,0,2,4,3,4],[0,3,1,4,2,0,0],[3,0,2,4,1,1,2],[0,2,1,3,4,3,1],[2,3,0,1,4,4,1],[0,4,1,3,2,1,1],[0,4,3,1,2,3,1],[0,3,1,2,4,3,1],[4,1,3,2,0,1,2],[3,1,0,2,4,3,1],[4,3,0,1,2,3,2],[1,3,2,0,4,1,3],[2,0,4,3,1,4,0],[2,2,1,4,3,0,0],[4,2,0,1,3,1,0],[0,4,3,2,1,3,0],[3,4,1,2,0,2,1],[0,3,2,1,4,1,3],[4,1,2,0,3,4,0],[2,4,1,0,3,1,0]]
                        
            Ro = [[1,2,3,0,4,4,1],[3,0,2,1,4,3,2],[3,1,0,4,2,3,1],[3,0,2,4,1,3,0],[4,0,2,3,1,2,1],[1,3,4,0,2,1,3],[2,4,3,1,0,1,0],[1,0,2,4,3,4,0],[3,0,2,1,4,4,0],[2,1,0,3,4,3,2],[3,1,2,4,0,3,1],[1,3,0,2,4,2,2],[0,3,4,2,1,1,2],[0,1,2,4,3,4,1],[2,0,3,4,1,0,4],[0,4,3,1,2,1,1],[2,0,1,3,4,2,1],[2,1,3,4,0,1,1],[3,4,1,0,2,1,2],[1,0,3,2,4,0,0],[3,1,0,4,2,0,0],[1,3,0,4,2,2,3],[1,0,3,4,2,2,3]]
            p = self.__randomInt(18)
            for x in range(5):            
                
                self.__addPit ( Co[p][x], Ro[p][x] )
                        

            # Generate wumpus
            wc = self.__randomInt(self.__colDimension)
            wr = self.__randomInt(self.__rowDimension)
            
            while wc == 0 and wr == 0:
                wc = self.__randomInt(self.__colDimension)
                wr = self.__randomInt(self.__rowDimension)
                
            self.__addWumpus ( Co[p][5], Ro[p][5] );
            
            # Generate gold
            gc = self.__randomInt(self.__colDimension)
            gr = self.__randomInt(self.__rowDimension)
                
            while (gc == 0 and gr == 0) or(wc==gc and wr==gr):
                gc = self.__randomInt(self.__colDimension)
                gr = self.__randomInt(self.__rowDimension)
            
            self.__addGold ( Co[p][6], Ro[p][6] )
            
        else:
            # Add the Wumpus
            c, r = [int(x) for x in next(file).split()]
            self.__addWumpus ( c, r )
            
            # Add the Gold
            c, r = [int(x) for x in next(file).split()]
            self.__addGold ( c, r )
            
            # Add the Pits
            numOfPits = int(next(file))
            
            while numOfPits > 0:
                numOfPits -= 1
                c, r = [int(x) for x in next(file).split()]
                self.__addPit ( c, r )
                
            file.close()
    
    def __addPit ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].pit = True
            self.__addBreeze ( c+1, r )
            self.__addBreeze ( c-1, r )
            self.__addBreeze ( c, r+1 )
            self.__addBreeze ( c, r-1 )
    
    def __addWumpus ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].wumpus = True
           
            self.__addStench ( c+1, r )
            self.__addStench ( c-1, r )
            self.__addStench ( c, r+1 )
            self.__addStench ( c, r-1 )
    
    def __addGold ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].gold = True
            
    
    def __addStench ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].stench = True
    
    def __addBreeze ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].breeze = True
    
    def __isInBounds ( self, c, r ):
        return c < self.__colDimension and r < self.__rowDimension and c >= 0 and r >= 0
    

    def __printGridInfo ( self ):
        self.__printBoardInfo()
        self.__printAgentInfo()
    
    def __printBoardInfo ( self ):
        for r in range (self.__rowDimension-1, -1, -1):
            for c in range (self.__colDimension):
                self.__printTileInfo ( c, r )
            print("")
            print("")

    def __printTileInfo ( self, c, r ):
        tileString = ""
        
        if self.__board[c][r].pit:
            tileString += "P"
            #print(c,",",r)
        if self.__board[c][r].wumpus:
            tileString += "W"
        if self.__board[c][r].gold:
            tileString += "G"
        if self.__board[c][r].breeze:
            tileString += "B"
        if self.__board[c][r].stench:
            tileString += "S"
        
        if self.__agentX == c and self.__agentY == r:
            if self.__agentDir == 0:
                tileString += "►"
            
            elif self.__agentDir == 1:
                tileString += "▼"
            
            elif self.__agentDir == 2:
                tileString += "◄"
            
            elif self.__agentDir == 3:
                tileString += "▲"
      
        
        tileString += " ○"
        
        print(tileString.rjust(8), end="")
    
    def __printAgentInfo ( self ):
    
        print ( "\t \t \t \t \t \t \t Agent Location X: "  + str(self.__agentX) )
        print ( "\t \t \t \t \t \t \t Agent Location Y: "  + str(self.__agentY) )
        self.__printDirectionInfo()
        self.__printActionInfo()
        self.__printPerceptInfo()
    
    def __printDirectionInfo ( self ):
        if self.__agentDir == 0:
            print ( "\t \t \t \t \t \t \t Agent Look Direction: Right" )
            
        elif self.__agentDir == 1:
            print ( "\t \t \t \t \t \t \t Agent Look Direction: Down" )
            
        elif self.__agentDir == 2:
            print ( "\t \t \t \t \t \t \t Agent Look Direction: Left" )
            
        elif self.__agentDir == 3:
            print ( "\t \t \t \t \t \t \t Agent Look Direction: Up" )
            
        else:
            print ( "\t \t \t \t \t \t \t Agent Look Direction: Invalid" )
    
    def __printActionInfo ( self ):
        if self.__lastAction == Agent.Action.TURN_LEFT:
            print ( "\t \t \t \t \t \t \t Last Action: Turned Left" )

        elif self.__lastAction == Agent.Action.TURN_RIGHT:
            print ( "\t \t \t \t \t \t \t Last Action: Turned Right")

        elif self.__lastAction == Agent.Action.FORWARD:
            print ( "\t \t \t \t \t \t \t Last Action: Moved Forward")

        elif self.__lastAction == Agent.Action.SHOOT:
            print ( "\t \t \t \t \t \t \t Last Action: Shot the Arrow")

        elif self.__lastAction == Agent.Action.GRAB:
            print ( "\t \t \t \t \t \t \t Last Action: Grabbed")

        elif self.__lastAction == Agent.Action.CLIMB:
            print ( "\t \t \t \t \t \t \t Last Action: Climbed")

        else:
            print ( "\t \t \t \t \t \t \t Last Action: Invalid")

    def __printPerceptInfo ( self ):
        perceptString = "\t \t \t \t \t \t \t Percepts: "
        
        if self.__board[self.__agentX][self.__agentY].stench: perceptString += "Stinks, "
        if self.__board[self.__agentX][self.__agentY].breeze: perceptString += "Strong Wind, "
        if self.__board[self.__agentX][self.__agentY].gold:   perceptString += "Gold, "
        if self.__bump:                         perceptString += "Bump, "
        if self.__scream:                       perceptString += "Scream"
        
        if perceptString[-1] == ' 'and perceptString[-2] == ',':
            perceptString = perceptString[:-2]
        
        print(perceptString)

    
    def __randomInt ( self, limit ):
        return random.randrange(limit)
