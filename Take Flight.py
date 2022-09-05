import pygame
import random

#Width and Height of Window
WIDTH = 600
HEIGHT = 700

#Displaying Window
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Take Flight")

#Importing, Scaling Background and Initializing Variables#
background_img = pygame.image.load("SKY.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
background_img2 = background_img
background_speed = 4 
background2y = HEIGHT * -1
background1y = 0

#Importing and Scaling Fireball#
fireball_img = pygame.image.load("FIREBALL.png")
FIREBALL_SIZE = (30, 80)
fireball_img = pygame.transform.scale(fireball_img, FIREBALL_SIZE)

#Importing, Scaling Hot-Air Balloon and Initializing Variables#
character_img = pygame.image.load("3 HP.png")
CHARACTER_SIZE = (85,135)
character_img = pygame.transform.scale(character_img, CHARACTER_SIZE)
x = 250
y = 450
balloon_speed = 5

#Importing Health-Upgrade#
healthup_img = pygame.image.load("HEALTH-UPGRADE.png")

#Importing and Scaling Strawberry Obstacle#
spritelist = ["STRAWBERRY-OBSTACLE.png","CARROT-OBSTACLE.png","BOOK-OBSTACLE.png","CONTROLLER-OBSTACLE.png"]

#Importing Lives and Initializing Variable#
lives3_img = pygame.image.load("HEALTH-BAR 3.png")
lives2_img = pygame.image.load("HEALTH-BAR 2.png")
lives1_img = pygame.image.load("HEALTH-BAR 1.png")
lives = 3

#Importing Score and Setting Multiplier for Score#
score_img = pygame.image.load("SCORE.png")
score = 0
counter = 0

#Initializing Fonts#
font1 = pygame.font.SysFont("agencyfb", 50, bold=True, italic=False)
font2 = pygame.font.SysFont("agencyfb", 30, bold=True, italic=False)
font3 = pygame.font.SysFont("agencyfb", 55, bold=True, italic=False)

#Importing Sprites for Menu Movement and Setting Variables(speed, x and y-coordinate)#
menu_img = pygame.image.load("MENU-PLANE 2.png")
menu_plane_speed = 5
plane1x = 600
menu_img2 = pygame.image.load("MENU-PLANE.png")
menu_plane_speed2 = 5
plane2x = -280
bird_menu = pygame.image.load("ExitGameMenu.png")
BIRD1_SIZE = (300, 285)
bird_menu = pygame.transform.scale(bird_menu, BIRD1_SIZE)
bird_menu_speed = 5
BirdY = 840

#Importing Sprites for Game-Over Movement and Setting Variables(speed, x and y-coordinate)#
menu_imgGO = pygame.image.load("GO-PLANE 2.png")
GO_plane_speed = 5
planeGO1x = 600
menu_imgGO2 = pygame.image.load("GO-PLANE.png")
GO_plane_speed2 = 5
planeGO2x = -280
GotoMenu = pygame.image.load("Go to MENU.png")
GotoMenuY = 700
GotoMenu_speed = 5
displayscore = pygame.image.load("DisplayScore.png")
displayscore_speed = 2.5
displayscoreY = -140

#Importing Sprites for Win Movement and Setting Variables(speed, x and y-coordinate)#
winTrophy_speed = 5
WinTrophy_img = pygame.image.load("trophy win.png")
WinTrophyY = -250
winGame_speed = 5
WinGame_img = pygame.image.load("game left.png")
WinGameX = -250
winOver_speed = 5
WinOver_img = pygame.image.load("over right.png")
WinOverX = 700
winWin_speed = 5
WinWin_img = pygame.image.load("you win.png")
WinWinY = 835

#Initializing Sound-Effects#
Click = pygame.mixer.Sound("Click Sound Effect.wav")
ball = pygame.mixer.Sound("Fireball Sound Effect.wav")
collidewithob = pygame.mixer.Sound("collision.wav")
collidewithheart = pygame.mixer.Sound("Healeffect.wav")
firewithob = pygame.mixer.Sound("FirewithOb.wav")
pygame.mixer.music.load("background music.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

#Initialize Movement/Mouse Variables#
up = False
right = False
down = False
left = False
space = False
mousePressed = False

#Creating Class for Strawberry Obstacle and Setting Variables#
class Object():
    def __init__(self, x, y, yspeed,spriteNum):
        self.x = x
        self.y = y
        self.w = 40
        self.h = 40
        self.yspeed = yspeed
        self.spriteNum = spriteNum
        self.sprite = 0
        self.name = "object"
        
    #Draw Function for Strawberry Image#
    def draw(self):
        self.name = pygame.image.load(spritelist[self.spriteNum])
        self.name = pygame.transform.scale(self.name,(40,55))
        screen.blit(self.name, (self.x, self.y))
        
    #Move Function for Strawberries to Increase in the Y-Position#
    def move(self):
        self.y += self.yspeed
        
#List Will Have All Appended Strawberries#        
objects = []

#Creating Class for Health Upgrade and Setting Variables#
class HealthUp():
    def __init__(self, x, y, w, h, yspeed):
        self.x = x
        self.y = y
        self.w = 40
        self.h = 40
        self.yspeed = yspeed
    
    #Draw Function for Health Upgrade Image#
    def draw(self):
        screen.blit(healthup_img, (self.x, self.y))
        
    #Move Function for Health Upgrade to Increase in the Y-Position#
    def move(self):
        self.y += self.yspeed

#List Will Have All Appended Health Upgrades#
healthups = []

#Creating Class for Fireball and Setting Variables#
class Fireball():
    def __init__(self, x, y, speedy, w, h):
        self.x = x
        self.y = y
        self.speedy = speedy
        self.w = w
        self.h = h

#List Will Have All Appended Individual Fireballs#
Fireballs = []
#Speed for Fireballs to Decrease in the Y-Position#
fireball_speed = 12

#Creating Function for Collision Between Obstacles and Player, Setting Variables and Compraing Them to Check for Collision#
def collision(x1, y1, w1, h1, x2, y2, w2, h2):
    if x1 + w1 < x2 or y1 + h1 < y2 or x1 > x2 + w2 or y1 > y2 + h2:
        return False
    else:
        return True
    
#Average Number of Collisions that happens between Player and Obstacle#
index = 5

#Starting Game in menu and Controlling the Game State#
gameState = "menu"

#Game loop
done = False
while True:
    # ===================== HANDLE EVENTS =================================== #
    for event in pygame.event.get():             
        if event.type == pygame.QUIT:
            pygame.quit()
            done = True
            break
        #Playing a Sound Every Time the Mouse is Clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mixer.Sound.play(Click)
            mousePressed = True    
        if event.type == pygame.MOUSEBUTTONUP: 
            mousePressed = False
            
        if event.type == pygame.KEYDOWN:      
            #If Key is Pressed#    
            if event.key == pygame.K_UP:      
                up = True
            if event.key == pygame.K_RIGHT:     
                right = True
            if event.key == pygame.K_LEFT:      
                left = True
            if event.key == pygame.K_DOWN:     
                down = True
            #Playing Sound and Appending Fireballs to Fireball list while putting in the paramaters for them# 
            if event.key == pygame.K_SPACE:
                space = True
                pygame.mixer.Sound.play(ball)
                Fireballs.append(Fireball(x+28,y+10,fireball_speed, 0, 0))


        
        if event.type == pygame.KEYUP:        
            #If Key is Not Pressed#    
            if event.key == pygame.K_UP:      
                up = False
            if event.key == pygame.K_RIGHT:    
                right = False
            if event.key == pygame.K_LEFT:      
                left = False
            if event.key == pygame.K_DOWN:    
                down = False
            if event.key == pygame.K_SPACE:
                space = False

    if done == True:
        break

        # ============================== MOVE STUFF ============================= #
    #Conditions for the Game if GameState is "inGame"#
    if gameState == "inGame":
        #Checking each Strawberry in List of Strawberries wether it collided with The Player or Not#
        for obj in objects:
            if collision(x, y, 85, 135, obj.x, obj.y, obj.w, obj.h):
                #If the Collision is True and the Number of Collisions is Equal to Five or More then Reduce Score, Lives and set Index to Zero so it Only Removes one Life#
                if collision == True or index >= 5:
                    pygame.mixer.Sound.play(collidewithob)
                    objects.remove(obj)
                    score -= 10
                    lives -= 1
                    index = 0
                    if lives == 2:
                        index = 5
                    if lives == 1:
                        index = 5
            for individualFireball in Fireballs:
                if collision(individualFireball.x, individualFireball.y, 30, 80, obj.x, obj.y,obj.w, obj.h):
                    if collision == True or index >= 5:
                        pygame.mixer.Sound.play(firewithob)
                        Fireballs.remove(individualFireball)
                        objects.remove(obj)
                        score += 5
                        index = 0
                        if lives == 3 or lives > 3:
                            index = 5
                        if lives == 2:
                            index = 5
                        if lives == 1:
                            index = 5
        #Removing strawberry from list if its Y Value is Greater than the Height to Reduce lag of Game#
        for obj in objects:
            if obj.y > HEIGHT:
                objects.remove(obj)
                
        #Checking each healthup in List of healthups wether it collided with The Player or Not# 
        for healthup in healthups:
            if collision(x, y, 85, 135, healthup.x, healthup.y, healthup.w, healthup.h):
                #If the Collision is True and the Number of Collisions is Equal to Five or More then Reduce Score, Lives and set Index to Zero so it Only Removes one Life#
                if collision == True or index >= 5:
                    pygame.mixer.Sound.play(collidewithheart)
                    healthups.remove(healthup)
                    lives += 1
                    index = 5
                    if lives == 3 or lives > 3:
                        lives = 3
            for individualFireball in Fireballs:        
                if collision(individualFireball.x, individualFireball.y, 30, 80, healthup.x, healthup.y,healthup.w, healthup.h):
                    if collision == True or index >= 5:
                        pygame.mixer.Sound.play(firewithob)
                        Fireballs.remove(individualFireball)
                        index = 5
                        
        #Removing healthup from list if its Y Value is Greater than the Height to Reduce lag of Game# 
        for healthup in healthups:
            if healthup.y > HEIGHT:
                healthups.remove(healthup)
                
        #Depending on Which Key is Pressed, The X andd Y value of the Ballon Increase#
        if left:
            x -= balloon_speed
        if right:
            x += balloon_speed
        if up:
            y -= balloon_speed
        if down:
            y += balloon_speed
        
        #Speed for Background#    
        background1y += background_speed
        background2y += background_speed
        
        #Speed for Fireballs# 
        for individualFireball in Fireballs:
            individualFireball.y -= fireball_speed
        
        # ============================== COLLISION ============================== #
    #Setting Conditions for when Game State is in Menu
    if gameState == "menu":
        mouseX, mouseY = pygame.mouse.get_pos()
        if mousePressed:
            #If in the menu and X coordinate was pressed in a specific range and and Y coordinate in another then game state would change to game#
            if 293 <= mouseX <= 442 and 303 <= mouseY <= 334:
                gameState = "inGame"
                mousePressed = False
                
            #If in the menu and X coordinate was pressed in a specific range and and Y coordinate in another then game state would change to instructions#
            if 148 <= mouseX <= 304 and 377 <= mouseY <= 407:
                gameState = "instructions"
                mousePressed = False
                
            #If in the menu and X coordinate was pressed in a specific range and and Y coordinate in another then game state would change to quit#    
            if 210 <= mouseX <= 390 and 530 <= mouseY <= 575:
                gameState = "quitGame"
                mousePressed = False
    
    #Setting Conditions for when player losses#
    if gameState == "gameOver":
        mouseX, mouseY = pygame.mouse.get_pos()
        if mousePressed:
            #If in the menu and X coordinate was pressed in a specific range and and Y coordinate in another then game state would change to menu, resetting all variables so player can start a new game#
            if 220 <= mouseX <= 400 and 440 <= mouseY <= 505:
                gameState = "menu"
                mousePressed = False
                objects = []
                Fireballs = []
                healthups = []
                lives = 3
                score = 0
                counter = 0
                fireball_speed = 12
                index = 5
                obstacle_speed = 5
                menu_plane_speed = 5
                plane1x = 600
                menu_plane_speed2 = 5
                plane2x = -280
                GO_plane_speed = 5
                planeGO1x = 600
                GO_plane_speed2 = 5
                planeGO2x = -280
                GotoMenuY = 700
                GotoMenu_speed = 5
                x = 250
                y = 450
                balloon_speed = 5
                background_speed = 4 
                background2y = HEIGHT * -1
                background1y = 0
                displayscore_speed = 2.5
                displayscoreY = -140
                bird_menu_speed = 5
                BirdY = 840
                winTrophy_speed = 5
                WinTrophyY = -250
                winGame_speed = 5
                WinGameX = -250
                winOver_speed = 5
                WinOverX = 700
                winWin_speed = 5
                WinWinY = 835
    
    #When in Instructions, tyhe user can press anywhere to go back to main menu#
    if gameState == "instructions":
        if mousePressed:
            gameState = "menu"
            mousePressed = False
    
    #Setting Conditions for when player is in the game#
    if gameState == "inGame":
        #If the user presses the mouse button anywhere, it will send them back to the main menu, resseting their progress#
        #resetting all variables so player can start a new game#
        if mousePressed:
            gameState = "menu"
            mousePressed = False
            objects = []
            Fireballs = []
            healthups = []
            lives = 3
            score = 0
            counter = 0
            fireball_speed = 12
            index = 5
            obstacle_speed = 5
            menu_plane_speed = 5
            plane1x = 600
            menu_plane_speed2 = 5
            plane2x = -280
            GO_plane_speed = 5
            planeGO1x = 600
            GO_plane_speed2 = 5
            planeGO2x = -280
            GotoMenuY = 700
            GotoMenu_speed = 5
            x = 250
            y = 450
            balloon_speed = 5
            background_speed = 4 
            background2y = HEIGHT * -1
            background1y = 0
            displayscore_speed = 2.5
            displayscoreY = -140
            bird_menu_speed = 5
            BirdY = 840
            winTrophy_speed = 5
            WinTrophyY = -250
            winGame_speed = 5
            WinGameX = -250
            winOver_speed = 5
            WinOverX = 700
            winWin_speed = 5
            WinWinY = 835
             
        #Looping through Background#
        if background1y >= HEIGHT:
            background1y = HEIGHT * -1
        if background2y >= HEIGHT:
            background2y = HEIGHT * -1
            
        #Border around Window#
        if x < 10:
            x = 10
        if x > WIDTH - 95:
            x = WIDTH - 95
        if y < 10:
            y = 10
        if y + 150 > HEIGHT:
            y = HEIGHT - 150
        
        
        #Score Multiplier to make it increase at a slower rate#
        counter += 1
        if score >= 100 and score < 200:
            for obj in objects:
                obj.yspeed += 0.025
        elif score >= 200 and score < 300:
            for obj in objects:
                obj.yspeed += 0.05
        elif score >= 300 and score < 400:
            for obj in objects:
                obj.yspeed += 0.075
        elif score >= 400 and score < 500:
            for obj in objects:
                obj.yspeed += 0.1
        elif score >= 500 and score < 600:
            for obj in objects:
                obj.yspeed += 0.125
        elif score >= 600 and score < 700:
            for obj in objects:
                obj.yspeed += 0.150
        elif score >= 700 and score < 800:
            for obj in objects:
                obj.yspeed += 0.175
        elif score >= 800 and score < 900:
            for obj in objects:
                obj.yspeed += 0.2
        elif score >= 900 and score < 1000:
            for obj in objects:
                obj.yspeed += 0.225
        
        #Changing gameState depending on score#
        if score >= 1000 :
            gameState = "win"
                
            
        #Creating Score Font#
        font = pygame.font.SysFont("agencyfb", 40, bold=True, italic=False)
        text = font.render(str(score), True, (0,0,0))
        
        # ============================== DRAW STUFF ============================= #
        #Setting Conditions for when player is in the game#
        if gameState == "inGame":
            screen.fill((255,255,255))
            #Displaying Background#
            screen.blit(background_img,(0,background1y))
            screen.blit(background_img2,(0,background2y))
            
            #Displaying Fireballs#
            for individualFireball in Fireballs:
                screen.blit(fireball_img,(individualFireball.x, individualFireball.y))
            
            #Displaying Character#
            screen.blit(character_img, (x,y))
            
            #Displaying Lives image dpeneding on health count#
            if lives == 3:
                screen.blit(lives3_img, (450,650))
            if lives == 2:
                screen.blit(lives2_img, (450,650))
            if lives == 1:
                screen.blit(lives1_img, (450,650))
            #Ending Game when User reaches 0 lives#
            if lives == 0:
                gameState = "gameOver"
                
            #Displaying Score Sprite and counter#   
            screen.blit(score_img, (10, 650))
            screen.blit(text, [110,643])
            
            #Displaying Strawberry Obstacle depending on score counter#
            if counter % 50 == 0:
                objects.append(Object(random.randint(10,550), -50, random.randint(5,8),random.randint(0,3)))
            #Applying Function for list#
            for obj in objects:
                obj.draw()
                obj.move()

            #Displaying Health Upgrade depending on score counter#
            if counter % 300 == 0:
                healthups.append(HealthUp(random.randint(10,530), -1000, 0, 0, random.randint(5,8)))
            #Applying Function for list#
            for healthup in healthups:
                healthup.draw()
                healthup.move()
                
    #Setting Conditions for when player wins#
    if gameState == "win":
        mouseX, mouseY = pygame.mouse.get_pos()
        #Animation for displaying player score#
        text = font.render(str(score), True, (0,0,0))
        screen.blit(background_img, (0,0))
        WinTrophyY += winTrophy_speed
        screen.blit(WinTrophy_img, (253,WinTrophyY))
        screen.blit(text, [268, WinTrophyY + 75])
        if WinTrophyY == 150:
            winTrophy_speed = 0
        
        #Animation for displaying player score#
        WinOverX -= winOver_speed
        screen.blit(WinOver_img, (WinOverX,275))
        if WinOverX == 300:
            winOver_speed = 0
        
        #Animation for displaying player score#
        WinGameX += winGame_speed
        screen.blit(WinGame_img, (WinGameX,275))
        if WinGameX == 140:
            winGame_speed = 0
        
        WinWinY -= winWin_speed
        screen.blit(WinWin_img, (240,WinWinY - 100))
        if WinWinY == 430:
            winWin_speed = 0
        
        #Animation for going to menu#
        GotoMenuY -= GotoMenu_speed
        screen.blit(GotoMenu, (150, GotoMenuY - 50))
        text = font2.render("Back to Menu", True, (0,0,0))
        screen.blit(text, [235, GotoMenuY + 135])
        if GotoMenuY == 370:
            GotoMenu_speed = 0
        if mousePressed:
            #If in the menu and X coordinate was pressed in a specific range and and Y coordinate in another then game state would change to menu, resetting all variables so player can start a new game#
            if 210 <= mouseX <= 385 and 495 <= mouseY <= 555:
                gameState = "menu"
                mousePressed = False
                objects = []
                Fireballs = []
                healthups = []
                lives = 3
                score = 0
                counter = 0
                fireball_speed = 12
                index = 5
                obstacle_speed = 5
                menu_plane_speed = 5
                plane1x = 600
                menu_plane_speed2 = 5
                plane2x = -280
                GO_plane_speed = 5
                planeGO1x = 600
                GO_plane_speed2 = 5
                planeGO2x = -280
                GotoMenuY = 700
                GotoMenu_speed = 5
                x = 250
                y = 450
                balloon_speed = 5
                background_speed = 4 
                background2y = HEIGHT * -1
                background1y = 0
                displayscore_speed = 2.5
                displayscoreY = -140
                bird_menu_speed = 5
                BirdY = 840
                winTrophy_speed = 5
                WinTrophyY = -250
                winGame_speed = 5
                WinGameX = -250
                winOver_speed = 5
                WinOverX = 700
                winWin_speed = 5
                WinWinY = 835
                
    
    #Setting Conditions for when player losses#
    if gameState == "gameOver":
        screen.blit(background_img, (0,0))
        
        #Animation for displaying player score#
        text = font.render(str(score), True, (0,0,0))
        displayscoreY += displayscore_speed
        screen.blit(displayscore, (210,displayscoreY))
        screen.blit(text, [285,displayscoreY + 35])
        if displayscoreY == 80:
            displayscore_speed = 0
        
        #Animation for text and plane#
        planeGO1x -= GO_plane_speed
        screen.blit(menu_imgGO, (planeGO1x,200))
        text = font2.render("GAME", True, (0,0,0))
        screen.blit(text, [planeGO1x + 180, 200])
        if planeGO1x == 160:
            GO_plane_speed = 0
        
        #Animation for text and plane#
        planeGO2x += GO_plane_speed2
        screen.blit(menu_imgGO2, (planeGO2x,250))
        text = font2.render("OVER", True, (0,0,0))
        screen.blit(text, [planeGO2x + 40, 250])
        if planeGO2x == 160:
            GO_plane_speed2 = 0
            
        #Animation for going to menu#
        GotoMenuY -= GotoMenu_speed
        screen.blit(GotoMenu, (160, GotoMenuY))
        text = font2.render("Back to Menu", True, (0,0,0))
        screen.blit(text, [245, GotoMenuY + 185])
        if GotoMenuY == 270:
            GotoMenu_speed = 0
    
    #Setting Conditions for when player is in menu#
    if gameState == "menu":
        screen.blit(background_img, (0,0))
        
        #Creating Title#
        text = font3.render("Take", True, (0,0,0))
        screen.blit(text, [185,200])
        text = font3.render("Flight", True, (0,0,0))
        screen.blit(text, [280,200])
        text = font1.render("Take", True, (255,255,255))
        screen.blit(text, [185,200])
        text = font1.render("Flight", True, (255,255,255))
        screen.blit(text, [280,200])
        
        #Animation for game plane#
        plane1x -= menu_plane_speed
        screen.blit(menu_img, (plane1x,300))
        text = font2.render("Start", True, (0,0,0))
        screen.blit(text, [plane1x + 180, 300])
        if plane1x == 160:
            menu_plane_speed = 0
        
        #Animation for Instructions plane#
        plane2x += menu_plane_speed
        screen.blit(menu_img2, (plane2x,375))
        text = font2.render("Instructions", True, (0,0,0))
        screen.blit(text, [plane2x + 13, 375])
        if plane2x == 0:
            menu_plane_speed2 = 0
        
        #Animation to quit the game#
        BirdY -= bird_menu_speed
        screen.blit(bird_menu, (150, BirdY))
        text = font2.render("QUIT GAME", True, (0,0,0))
        screen.blit(text, [245, BirdY + 137])
        if BirdY == 395:
            bird_menu_speed = 0
    
    #Setting Conditions for when player is in instructions#
    if gameState == "instructions":
        screen.blit(background_img, (0,0))
        text = font1.render("Instructions", True, (0,0,0))
        screen.blit(text, [200,50])
        text = font2.render("1. Shoot obstacles in the way to gain points or lose a life", True, (0,0,0))
        screen.blit(text, [25, 120])
        text = font2.render("2. Collect a health generator on your way to use", True, (0,0,0))
        screen.blit(text, [25, 170])
        text = font2.render("for an advantage", True, (0,0,0))
        screen.blit(text, [25, 210])
        text = font2.render("3. Lose all your health and your balloon will pop", True, (0,0,0))
        screen.blit(text, [25, 250])
        text = font1.render("How To Play", True, (0,0,0))
        screen.blit(text, [200,310])
        text = font2.render("1. Use arrow keys to move", True, (0,0,0))
        screen.blit(text, [25, 380])
        text = font2.render("2. Press space to shoot fireballs", True, (0,0,0))
        screen.blit(text, [25, 420])
        text = font2.render("3. Click anywhere with the mouse to return to the", True, (0,0,0))
        screen.blit(text, [25, 460])
        text = font2.render("main menu to restart", True, (0,0,0))
        screen.blit(text, [25, 500])
    
    #Setting Conditions for when player clicks Wuit Game#
    if gameState == "quitGame":
        pygame.quit()
        
#     # ====================== PYGAME STUFF (DO NOT EDIT) ===================== #
    pygame.display.flip()
    pygame.time.delay(20)