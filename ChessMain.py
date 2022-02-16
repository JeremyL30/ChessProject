import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512  #Board size in pixels og:512
DIMENSION = 8 #dimension of 8x8 board
SQ_SIZE = HEIGHT // DIMENSION  #size per square
MAX_FPS = 15 #for animation
IMAGES = {}

#Initialize global dictionary of images. This will be called once
def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wK", "wQ", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

#Will be the main driver for handling user input and graphics
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    loadImages() #only once, before the while loop
    running = True
    sqSelected = () #initially no square is selected, keeps track of last click (tuple: (row,col))
    playersClick = [] #keeps track of the players clicks (two tuples: [(6, 4), (4, 4)

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse input
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #the user clicked the same square twice
                    sqSelected = () #deselect
                    playersClick = [] #clears players clicks
                else:
                    sqSelected = (row, col)
                    playersClick.append(sqSelected) #we append for the first and second click
                if len(playersClick) == 2: #after 2nd click
                    Move = ChessEngine.Move(playersClick[0], playersClick[1], gs.board)
                    print(Move.getChessNotation())
                    if Move in validMoves:
                        gs.makeMove(Move)
                        moveMade = True
                    sqSelected = () #reset user clicks
                    playersClick = []
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo z when pressed
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


#Responsible for all game grpahics
def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on the board
    drawPieces(screen, gs.board) #draw pieces on top of squares

def drawBoard(screen): #Draw squares on board
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
def drawPieces(screen, board): #Draw pieces on board related to the currrent Game state variable
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



if __name__ == "__main__":
    main()




