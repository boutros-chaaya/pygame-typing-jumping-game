import pygame
import sys


pygame.init()
window = pygame.display.set_mode((500, 500)) 

def set_text(string, coordx, coordy, fontSize): #Function to set text

    font = pygame.font.Font('freesansbold.ttf', fontSize) 
    #(0, 0, 0) is black, to make black text
    text = font.render(string, True, (0, 0, 0)) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 
    return (text, textRect)

run = True
while run:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				run = False
	
	window.fill((255, 255, 255)) #Fills the whole window with white
	#Places "Text in Pygame!" with an x,y coord of 250, 250 and 60 font size
	totalText = set_text("Text in Pygame!", 250, 250, 30)
	window.blit(totalText[0], totalText[1])
	pygame.display.update()
	
	
pygame.quit()
sys.exit()
