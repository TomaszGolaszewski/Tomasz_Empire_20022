import pygame

# from settings import *
from setup import *
from functions_math import *
from functions_player import *


class Base_page:
    def __init__(self, lvl_of_page, number_of_page, name):
    # initialization of the object

        # basic variables
        self.is_active = False
        self.name = name

        # variables for managing the graphics window
        # horizontally
        margin = 200
        title_width = 100
        # vertically
        origin_vert_pos = WIN_HEIGHT // 2      
        title_height = 25
        gap_between_lvls = 7
        origin_vert_pos_of_this_page = origin_vert_pos + lvl_of_page * (title_height + gap_between_lvls)
        margin_bottom = 50
        height_of_this_page = WIN_HEIGHT - origin_vert_pos_of_this_page - margin_bottom
        
        self.title_rect = pygame.Rect(margin + number_of_page * title_width, origin_vert_pos_of_this_page, title_width, title_height)
        self.page_rect = pygame.Rect(margin, origin_vert_pos_of_this_page + title_height, WIN_WIDTH - 2 * margin, height_of_this_page)

        # fonts
        font_arial_20 = pygame.font.SysFont('arial', 20)
        self.name_text = font_arial_20.render(self.name, True, LIME)
        self.name_text_rect = self.name_text.get_rect(center = self.title_rect.center)

    def draw(self, win):
    # draw the object on the screen    
        # background
        pygame.draw.rect(win, BLACK, self.title_rect)
        if self.is_active: pygame.draw.rect(win, BLACK, self.page_rect)
        # lines of title bar
        pygame.draw.line(win, LIME, self.title_rect.bottomleft, self.title_rect.topleft, 3) # left
        pygame.draw.line(win, LIME, self.title_rect.topleft, self.title_rect.topright, 3) # top
        pygame.draw.line(win, LIME, self.title_rect.topright, self.title_rect.bottomright, 3) # right
        # lines of page
        if self.is_active:
            pygame.draw.line(win, LIME, self.title_rect.bottomright, self.page_rect.topright, 3) # top_right
            pygame.draw.line(win, LIME, self.page_rect.topright, self.page_rect.bottomright, 3) # right
            pygame.draw.line(win, LIME, self.page_rect.bottomright, self.page_rect.bottomleft, 3) # bottom
            pygame.draw.line(win, LIME, self.page_rect.bottomleft, self.page_rect.topleft, 3) # left
            pygame.draw.line(win, LIME, self.page_rect.topleft, self.title_rect.bottomleft, 3) # top_left
        # draw title   
        win.blit(self.name_text, self.name_text_rect.topleft)

    def press_left(self, list_with_units, press_coord):
    # handle actions after left button is pressed
        pass

    def press_right(self, *args):
    # handle actions after right button is pressed
        pass

    def is_title_pressed(self, press_coord):
    # check if title is pressed
    # return True if yes
        if self.title_rect.collidepoint(press_coord): return True
        else: return False
        
    def is_page_pressed(self, press_coord):
    # check if page is pressed
    # return True if yes
        if self.page_rect.collidepoint(press_coord): return True
        else: return False
        

class Page_with_notebook(Base_page):
    Pages_class = [Base_page, Base_page]

    def __init__(self, lvl_of_page, number_of_page, name):
        Base_page.__init__(self, lvl_of_page, number_of_page, name)

        # initialization of tabs
        self.list_with_pages = []
        number_of_page = 0
        for page_class in self.Pages_class:
            self.list_with_pages.append(page_class(lvl_of_page + 1, number_of_page, 'temp'))
            number_of_page += 1
        self.list_with_pages[0].is_active = True

    def draw(self, win):
    # draw the object on the screen  
        Base_page.draw(self, win)
        if self.is_active:
            for page in self.list_with_pages:
                page.draw(win)

    def press_left(self, list_with_units, press_coord):
    # handle actions after left button is pressed

        # check and handle actions after one of titles button is pressed
        was_some_title_pressed = False
        for page in self.list_with_pages:
            if page.is_title_pressed(press_coord): was_some_title_pressed = True
        if was_some_title_pressed:
            for page in self.list_with_pages:
                page.is_active = False
                if page.is_title_pressed(press_coord):
                    page.is_active = True

        # check and handle actions after one of pages is pressed
        for page in self.list_with_pages:
            if page.is_active and page.is_page_pressed(press_coord):
                page.press_left(list_with_units, press_coord)


# ======================================================================


class Base_notebook:
    Pages_class = [Base_page, Page_with_notebook, Base_page]

    def __init__(self):
    # initialization of the object

        # basic variables
        self.to_remove = False

        # initialization of tabs
        self.list_with_pages = []
        number_of_page = 0
        for page_class in self.Pages_class:
            self.list_with_pages.append(page_class(0, number_of_page, 'temp_name'))
            number_of_page += 1
        self.list_with_pages[0].is_active = True

    def draw(self, win):
    # draw the object on the screen
        for page in self.list_with_pages:
            page.draw(win)

    def press_left(self, list_with_units, press_coord):
    # handle actions after left button is pressed
        was_pressed = False
        for page in self.list_with_pages:
            if was_pressed: page.is_active = False # previous page was activated
            if page.is_active:
                if page.is_title_pressed(press_coord): # title of active tab is pressed
                    was_pressed = True
                elif page.is_page_pressed(press_coord): # page (body) is pressed
                    was_pressed = True
                    page.press_left(list_with_units, press_coord)
                else: # nothing on this tab has been pressed
                    page.is_active = False
            else:
                if page.is_title_pressed(press_coord): # title of inactive tab is pressed
                    was_pressed = True
                    page.is_active = True

        if not was_pressed: self.to_remove = True # nothing on this notebook has been pressed

    def press_right(self, *args):
    # handle actions after right button is pressed
        pass
    

# ======================================================================


class Base_slide_button:
    path = BUTTON_1_PATH

    def __init__(self, coord):
    # initialization of the object

        # basic variables
        self.coord = coord
        self.to_remove = False

        # load and prepare sprite
        self.sprite = pygame.image.load(os.path.join(*self.path))
        self.sprite.convert()
        # self.sprite.convert_alpha()
        self.sprite.set_colorkey(BLACK)
        # self.sprite.set_alpha(50)

        # calculate frame size
        sprite_rect = self.sprite.get_rect()
        self.frame_width = sprite_rect.width
        self.frame_height = sprite_rect.height

    def draw(self, win):
    # draw the object on the screen
        new_rect = self.sprite.get_rect(center = self.coord)
        win.blit(self.sprite, new_rect.topleft)

    def press_left(self, *args):
    # handle actions after left button is pressed
        pass

    def press_right(self, list_with_units, press_coord, target, is_ctrl_down):
    # handle actions after right button is pressed
        # check if center is pressed
        dist = math.hypot(self.coord[0]-press_coord[0], self.coord[1]-press_coord[1])
        if dist < 25:
            # print("center")
            set_new_target_move(list_with_units, target, is_ctrl_down)
        else:
            # check sector       
            angle = math.degrees(angle_to_target(self.coord, press_coord))
            if angle < 270 and angle > 90:
                # print("left")
                set_new_target_regroup(list_with_units, target, is_ctrl_down)
            else:
                # print("right")
                set_new_target_move(list_with_units, target, is_ctrl_down)
        print()
        self.to_remove = True