# import
import sys
import time
import random
import os

import pygame as pg
from pygame.locals import Color, QUIT, MOUSEBUTTONDOWN, USEREVENT, USEREVENT
from pygame import *
from time import sleep


# 使用變數先指定參數
WINDOW_WIDTH = 300  # 遊戲畫面寬和高
WINDOW_HEIGHT = 300
WHITE = (255, 255, 255)
IMAGEWIDTH = 64
IMAGEHEIGHT = 64
FPS = 45

# pygame初始化
pg.init()


# 指定全域變數，物件
table = [[0 for i in range(4)] for i in range(4)]
newItemTable = [[0 for i in range(4)] for i in range(4)]
moveTable = [[0 for i in range(4)] for i in range(4)]
oldTable = [[0 for i in range(4)] for i in range(4)]
spriteTable = [[] for i in range(4)]
imgTable = {0: [], 2: [], 4: [], 8: [], 16: [], 32: [], 64: [],
            128: [], 256: [], 512: [], 1024: [], 2048: []}
allSprite = pg.sprite.Group()
font = pg.font.Font(os.path.join('2048ByNCC', 'HanyiSentyCrayon.ttf'), 24)


class Background(pg.sprite.Sprite):  # background的精靈類別
    def __init__(self, image_file, location):
        super().__init__()  # call Sprite initializer
        self.raw_image = pg.image.load(image_file).convert_alpha()
        self.image = pg.transform.smoothscale(self.raw_image, (300, 300))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.width = 300
        self.height = 300


class block(pg.sprite.Sprite):  # 每個Block的精靈類別
    def __init__(self, width, height, x, y, image_index):
        super().__init__()
        # 載入圖片
        self.image = imgTable[image_index][0]
        # 回傳位置
        self.rect = self.image.get_rect()
        # 定位
        self.rect.topleft = (x, y)
        self.width = width
        self.height = height

    def update(self, i, j, direction, finishAnimation, finishMoveAnimation):
        global moveTable
        global table
        global newItemTable
        global oldTable
        bx, by = self.rect.topleft
        if finishAnimation:
            self.rect.topleft = (10+64*j+8*j+1, 10+64*i+8*i)
            # 先移回來 10+64*j+8*j, 10+64*i+8*i
            self.image = imgTable[table[i][j]][0]
        else:
            if not finishMoveAnimation:
                if moveTable[i][j] != 0:
                    if direction == 1:  # up
                        self.rect.topleft = (bx, by-18)
                    elif direction == 2:  # down
                        self.rect.topleft = (bx, by+18)
                    elif direction == 3:  # left
                        self.rect.topleft = (bx-18, by)
                    else:  # right
                        self.rect.topleft = (bx+18, by)
                    moveTable[i][j] -= 0.25
                    self.image = imgTable[oldTable[i][j]][0]
            else:
                if moveTable[i][j] == 0:
                    if newItemTable[i][j] != 0:
                        newItemTable[i][j] -= 0.25
                        wah = int(newItemTable[i][j]/0.25 + 1)
                        self.rect.topleft = ( 
                            10+64*j+8*j+(32-8*(4-wah)), 10+64*i+8*i+(32-8*(4-wah)))
                        # 先移回來 10+64*j+8*j, 10+64*i+8*i
                        self.image = imgTable[table[i][j]][5-wah]
                    else:
                        self.rect.topleft = (10+64*j+8*j+1, 10+64*i+8*i)
                        self.image = imgTable[table[i][j]][0]

            # 一格花4次跑到，最後花4次放大縮小圖片，一次移動18px，


# 設定視窗
main_clock = pg.time.Clock()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# 依設定顯示視窗
pg.display.set_caption("2048 by ncc")
# 設定程式標題
BackGround = Background(os.path.join('2048ByNCC', 'bg.png'), [
    0, 0])  # 指定background物件


def RandomNewItem():
    while True:
        for i in range(3, -1, -1):  # y
            for j in range(4):  # x
                if table[i][j] == 0:
                    if random.randint(1, 16) == 1:
                        if random.random() > 0.5:
                            table[i][j] = 2
                        else:
                            table[i][j] = 4
                        return i, j


def init():
    # 亂數兩格來
    rn = random.randint(1, 4)  # randomNumber 三種機緣任君挑選
    if rn == 1:
        position = random.randint(8, 16)-1
        table[position % 4][position//4] = 2
        position = random.randint(1, position)-1
        table[position % 4][position//4] = 2
    elif rn == 2:
        position = random.randint(8, 16)-1
        table[position % 4][position//4] = 4
        position = random.randint(1, position)-1
        table[position % 4][position//4] = 2
    else:
        position = random.randint(8, 16)-1
        table[position % 4][position//4] = 2
        position = random.randint(1, position)-1
        table[position % 4][position//4] = 4

    # 先產生圖片的list
    for i in range(1, 12, 1):
        image_file = os.path.join('2048ByNCC', str(pow(2, i))+'.png')
        tmpRawImg = pg.image.load(image_file).convert_alpha()
        tmpImg = pg.transform.smoothscale(tmpRawImg, (IMAGEWIDTH, IMAGEHEIGHT))
        imgTable[pow(2, i)].append(tmpImg)
        for j in range(4):
            tmpImg = pg.transform.smoothscale(tmpRawImg, ((j)*16, (j)*16))
            imgTable[pow(2, i)].append(tmpImg)
    # 0的另外加
    image_file = os.path.join('2048ByNCC', '0.png')
    tmpRawImg = pg.image.load(image_file).convert_alpha()
    tmpImg = pg.transform.smoothscale(tmpRawImg, (IMAGEWIDTH, IMAGEHEIGHT))
    imgTable[0].append(tmpImg)
    for j in range(4):
        tmpImg = pg.transform.smoothscale(tmpRawImg, ((j)*16, (j)*16))
        imgTable[0].append(tmpImg)

    for i in range(4):
        for j in range(4):
            spriteTable[i].append(
                block(IMAGEWIDTH, IMAGEHEIGHT, 10+64*j+8*j+1, 10+64*i+8*i, table[i][j]))
            allSprite.add(spriteTable[i][j])


# TheIndex !
# 0,0 0,1 0,2 0,3
# 1,0 1,1 1,2 1,3
# 2,0 2,1 2,2 2,3
# 3,0 3,1 3,2 3,3


def showGameOver():
    # 加畫字
    print("GameOver!")
    while True:
        background2 = Background(os.path.join('2048ByNCC', 'background.png'), [
            0, 0])  # 指定background2物件
        text = font.render("哈哈，你輸惹，偶是念誠", True, (255, 255, 255))
        text2 = font.render("按[ENTER]重玩、[ESC]關掉", True, (255, 255, 255))

        for event in pg.event.get():
            if event.type == pg.QUIT:  # 關閉程式的判斷
                return  # 關閉程式的程式碼

        keys = pg.key.get_pressed()
        if keys[K_ESCAPE]:
            print("exiting")
            return
        if keys[K_RETURN]:
            print("Restarting")
            os.execl(sys.executable, sys.executable, *sys.argv)
        screen.blit(background2.image, background2.rect)
        screen.blit(text, (20, 20))
        screen.blit(text2, (20, 80))
        pg.display.update()
        main_clock.tick(FPS)
    # os.execl(sys.executable, sys.executable, *sys.argv)


def noMoreStep(table):
    fulled = True
    for i in range(4):  # y
        for j in range(4):  # x
            if table[i][j] == 0:
                fulled = True
                break
    if fulled:
        for i in range(3, 0, -1):  # y
            for j in range(4):  # x
                if table[i][j] != 0:
                    if table[i-1][j] == table[i][j]:
                        return False
                    if table[i-1][j] == 0:
                        return False
        for i in range(3):  # y
            for j in range(4):  # x
                if table[i][j] != 0:
                    if table[i+1][j] == table[i][j]:
                        return False
                    if table[i+1][j] == 0:
                        return False
        for i in range(3, 0, -1):  # x
            for j in range(4):  # y
                if table[j][i] != 0:
                    if table[j][i-1] == table[j][i]:
                        return False
                    if table[j][i-1] == 0:
                        return False
        for i in range(3):  # x
            for j in range(4):  # y
                if table[j][i] != 0:
                    if table[j][i+1] == table[j][i]:
                        return False
                    if table[j][i+1] == 0:
                        return False
        return True


def movable(table, direction):
    if direction == 1:
        for i in range(3, 0, -1):  # y
            for j in range(4):  # x
                if table[i][j] != 0:
                    if table[i-1][j] == table[i][j]:
                        return True
                    if table[i-1][j] == 0:
                        return True

    elif direction == 2:
        for i in range(3):  # y
            for j in range(4):  # x
                if table[i][j] != 0:
                    if table[i+1][j] == table[i][j]:
                        return True
                    if table[i+1][j] == 0:
                        return True
    elif direction == 3:
        for i in range(3, 0, -1):  # x
            for j in range(4):  # y
                if table[j][i] != 0:
                    if table[j][i-1] == table[j][i]:
                        return True
                    if table[j][i-1] == 0:
                        return True
    else:
        for i in range(3):  # x
            for j in range(4):  # y
                if table[j][i] != 0:
                    if table[j][i+1] == table[j][i]:
                        return True
                    if table[j][i+1] == 0:
                        return True
    return False


def move(direction):
    global moveTable
    global table
    global oldTable
    for i in range(4):
        for j in range(4):
            newItemTable[i][j] = 0
            moveTable[i][j] = 0
            oldTable[i][j] = table[i][j]
    needMove = [[True for i in range(4)]for j in range(4)]
    if direction == 1:  # up
        # 由上到下，左到右，先排好
        for i in range(1, 4, 1):  # y
            for j in range(4):  # x
                if (table[i][j] != 0):
                    for k in range(i-1, -1, -1):  # 由下到上
                        if table[k][j] == 0:
                            table[k][j] = table[k+1][j]
                            table[k+1][j] = 0
                            if k == 0:
                                moveTable[i][j] += i-k
                        elif table[k][j] != 0:
                            moveTable[i][j] += i-k-1
                            break

        print("up")
        # 由下到上，左到右，作檢查
        for i in range(3, 0, -1):  # y
            for j in range(4):  # x
                if needMove[i][j]:
                    if table[i][j] == table[i-1][j] and table[i][j] != 0:
                        # moveTable[i][j]+=1
                        table[i-1][j] *= 2
                        newItemTable[i-1][j] = 1
                        needMove[i-1][j] = False
                        table[i][j] = 0

        # 由上到下，左到右，整理好
        for i in range(1, 4, 1):  # y
            for j in range(4):  # x
                if (table[i][j] != 0):
                    if table[i-1][j] == 0:
                        table[i-1][j] = table[i][j]
                        table[i][j] = 0
                        # moveTable[i][j]+=i-1-k
                        if newItemTable[i][j] == 1:  # 排改變位置的表格
                            newItemTable[i-1][j] = 1
                            newItemTable[i][j] = 0

    elif direction == 2:
        # 由下到上，左到右，先排好
        for i in range(2, -1, -1):  # y
            for j in range(4):  # x
                if (table[i][j] != 0):
                    for k in range(i+1, 4, 1):  # 由上到下
                        if table[k][j] == 0:
                            table[k][j] = table[k-1][j]
                            table[k-1][j] = 0
                            if k == 3:
                                moveTable[i][j] += k-i
                        elif table[k][j] != 0:
                            moveTable[i][j] += k-i-1
                            break

        print("down")
        # 由上到下，左到右，作檢查
        for i in range(3):  # y
            for j in range(4):  # x
                if needMove[i][j]:
                    if table[i][j] == table[i+1][j] and table[i][j] != 0:
                        # moveTable[i][j]+=1
                        table[i+1][j] *= 2
                        newItemTable[i+1][j] = 1
                        needMove[i+1][j] = False
                        table[i][j] = 0

        # 由下到上，左到右，整理好
        for i in range(2, -1, -1):  # y
            for j in range(4):  # x
                if (table[i][j] != 0):
                    if table[i+1][j] == 0:
                        table[i+1][j] = table[i][j]
                        table[i][j] = 0
                        # moveTable[i][j]+=i-1-k
                        if newItemTable[i][j] == 1:  # 排改變位置的表格
                            newItemTable[i+1][j] = 1
                            newItemTable[i][j] = 0

    elif direction == 3:
        # 由左到又，由上到下，先排好
        for i in range(1, 4, 1):  # x
            for j in range(4):  # y
                if (table[j][i] != 0):
                    for k in range(i-1, -1, -1):  # 由又到左 k=>x
                        if table[j][k] == 0:
                            table[j][k] = table[j][k+1]
                            table[j][k+1] = 0
                            if k == 0:
                                moveTable[j][i] += i-k
                        elif table[j][k] != 0:
                            moveTable[j][i] += i-k-1
                            break

        print("left")
        # 由又到左，由上到下，作檢查
        for i in range(3, 0, -1):  # x
            for j in range(4):  # y
                if needMove[j][i]:
                    if table[j][i] == table[j][i-1] and table[j][i] != 0:
                        # moveTable[i][j]+=1
                        table[j][i-1] *= 2
                        newItemTable[j][i-1] = 1
                        needMove[j][i-1] = False
                        table[j][i] = 0

        # 由左到又，由上到下，整理好
        for i in range(1, 4, 1):  # x
            for j in range(4):  # y
                if (table[j][i] != 0):
                    if table[j][i-1] == 0:
                        table[j][i-1] = table[j][i]
                        table[j][i] = 0
                        # moveTable[i][j]+=i-1-k
                        if newItemTable[j][i] == 1:  # 排改變位置的表格
                            newItemTable[j][i-1] = 1
                            newItemTable[j][i] = 0

    else:
        # 由又到左，由上到下，先排好
        for i in range(2, -1, -1):  # x
            for j in range(4):  # y
                if (table[j][i] != 0):
                    for k in range(i+1, 4, 1):  # 由左到又移動 k=>x
                        if table[j][k] == 0:
                            table[j][k] = table[j][k-1]
                            table[j][k-1] = 0
                            if k == 3:
                                moveTable[j][i] += k-i
                        elif table[j][k] != 0:
                            moveTable[j][i] += k-i-1
                            break

        print("right")
        # 由左到又，由上到下，作檢查
        for i in range(3):  # x
            for j in range(4):  # y
                if needMove[j][i]:
                    if table[j][i] == table[j][i+1] and table[j][i] != 0:
                        # moveTable[i][j]+=1
                        table[j][i+1] *= 2
                        newItemTable[j][i+1] = 1
                        needMove[j][i+1] = False
                        table[j][i] = 0

        # 由又到左，由上到下，整理好
        for i in range(2, -1, -1):  # x
            for j in range(4):  # y
                if (table[j][i] != 0):
                    if table[j][i+1] == 0:
                        table[j][i+1] = table[j][i]
                        table[j][i] = 0
                        # moveTable[i][j]+=i-1-k
                        if newItemTable[j][i] == 1:  # 排改變位置的表格
                            newItemTable[j][i+1] = 1
                            newItemTable[j][i] = 0

    x, y = RandomNewItem()
    newItemTable[x][y] = 1


def main():
    init()
    global Background
    global table
    direction = 0
    finishAnimation = True
    finishMoveAnimation = False
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # 關閉程式的判斷
                return
        if not finishAnimation:
            for i in range(4):  # y
                for j in range(4):  # x
                    spriteTable[i][j].update(
                        i, j, direction, finishAnimation, finishMoveAnimation)

            AMAF = False
            AAF = False
            finishMoveAnimation = False
            for i in range(3, -1, -1):  # y
                for j in range(4):  # x
                    if moveTable[i][j] == 0:
                        AMAF = True
                    else:
                        AMAF = False
                        break
                if not AMAF:
                    break
            for i in range(3, -1, -1):  # y
                for j in range(4):  # x
                    if newItemTable[i][j] == 0 and moveTable[i][j] == 0:
                        AAF = True
                    else:
                        AAF = False
                        break
                if not AAF:
                    break
            if AMAF:
                finishMoveAnimation = True
            if AAF:
                finishAnimation = True

#            print("MoveTable:")
#            for k in range(4):#y
#                for w in range(4):#x
#                    print(moveTable[k][w],end=" ")
#                print()
#            print(" Table:")
#            for i in range(4):#y
#                for j in range(4):#x
#                    print(table[i][j],end=" ")
#                print()
#            print("newItemTable")
#            for i in range(4):#y
#                for j in range(4):#x
#                    print(newItemTable[i][j],end=" ")
#                print()

        elif finishMoveAnimation and finishAnimation:
            for i in range(4):  # y
                for j in range(4):  # x
                    spriteTable[i][j].update(
                        i, j, direction, finishAnimation, finishMoveAnimation)
            finishMoveAnimation = False
            if noMoreStep(table):
                for i in range(4):  # y
                    for j in range(4):  # x\
                        table[i][j] = 0
                        spriteTable[i][j].update(i, j, direction, True, True)
                # Background.update(os.path.join('2048ByNCC', 'background.png')) #指定background物件
                sleep(2)
                showGameOver()
                return
        else:
            keys = pg.key.get_pressed()
            if keys[K_UP]:
                direction = 1
            if keys[K_DOWN]:
                direction = 2
            if keys[K_LEFT]:
                direction = 3
            if keys[K_RIGHT]:
                direction = 4

            if keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT]:
                if movable(table, direction):
                    move(direction)
                    finishAnimation = False
                else:
                    print("can't move this step!")

        screen.blit(BackGround.image, BackGround.rect)
        allSprite.draw(screen)
        pg.display.update()
        main_clock.tick(FPS)


if __name__ == '__main__':
    main()
    # 關閉程式的程式碼
    pg.quit()
