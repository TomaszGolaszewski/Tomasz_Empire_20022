import pygame

# from settings import *
from setup import *
from settings import *
from functions_math import *
from functions_player import *


class Base_window:
    def __init__(self):
        # basic variables
        self.to_remove = False

    def draw(self, win, dict_with_units):
    # draw the object on the screen
        pass

    def press_left(self, *args):
    # handle actions after left button is pressed
        pass

    def press_right(self, *args):
    # handle actions after right button is pressed
        pass


# ======================================================================


class Base_page:
    def __init__(self, id, lvl_of_page, number_of_page, name):
    # initialization of the object

        # basic variables
        self.id = id
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
        margin_bottom = 125
        height_of_this_page = WIN_HEIGHT - origin_vert_pos_of_this_page - margin_bottom
        
        self.title_rect = pygame.Rect(margin + number_of_page * title_width, origin_vert_pos_of_this_page, title_width, title_height)
        self.page_rect = pygame.Rect(margin, origin_vert_pos_of_this_page + title_height, WIN_WIDTH - 2 * margin, height_of_this_page - title_height)

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

    def press_left(self, dict_with_units, press_coord):
    # handle actions after left button is pressed
        pass

    # def press_right(self, *args):
    # # handle actions after right button is pressed
    #     pass

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

    def __init__(self, id, lvl_of_page, number_of_page, name):
        Base_page.__init__(self, id, lvl_of_page, number_of_page, name)

        # initialization of tabs
        self.list_with_pages = []
        number_of_page = 0
        for page_class in self.Pages_class:
            self.list_with_pages.append(page_class(id, lvl_of_page + 1, number_of_page, 'temp'))
            number_of_page += 1
        self.list_with_pages[0].is_active = True

    def draw(self, win):
    # draw the object on the screen  
        Base_page.draw(self, win)
        if self.is_active:
            for page in self.list_with_pages:
                page.draw(win)

    def press_left(self, dict_with_units, press_coord):
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
                page.press_left(dict_with_units, press_coord)


# ======================================================================


class Base_notebook:
    Pages_class = [Base_page, Page_with_notebook, Base_page]

    def __init__(self, id):
    # initialization of the object

        # basic variables
        self.id = id
        self.to_remove = False

        # initialization of tabs
        self.list_with_pages = []
        number_of_page = 0
        for page_class in self.Pages_class:
            self.list_with_pages.append(page_class(id, 0, number_of_page, 'temp_name'))
            number_of_page += 1
        self.list_with_pages[0].is_active = True

    def draw(self, win, dict_with_unit):
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


class Building_queue(Base_window):
    def __init__(self, id):
        # basic variables
        self.to_remove = False
        # basic data about unit
        self.id = id  
        # variables for managing the graphics window    
        # vertically
        bottom_margin = 25
        self.field_size = 75
        origin_vert_pos = WIN_HEIGHT - bottom_margin - self.field_size 
        # horizontally
        self.queue_slots = 10
        window_width = self.queue_slots * self.field_size
        origin_horz_pos = (WIN_WIDTH - window_width) // 2
        self.window_rect = pygame.Rect(origin_horz_pos, origin_vert_pos, window_width, self.field_size)

    def draw(self, win, dict_with_units):
    # draw windows with unit's queue
        if self.id in dict_with_units:
            if dict_with_units[self.id].is_selected:
                # background
                pygame.draw.rect(win, BLACK, self.window_rect)
                # lines of title bar
                pygame.draw.line(win, LIME, self.window_rect.topleft, self.window_rect.topright, 3) # top
                pygame.draw.line(win, LIME, self.window_rect.bottomright, self.window_rect.bottomleft, 3) # bottom
                origin = self.window_rect.topleft
                for i in range(self.queue_slots + 1):         
                    pygame.draw.line(win, LIME, (origin[0] + i * self.field_size, origin[1]), (origin[0] + i * self.field_size, origin[1] + self.field_size), 3)      
            else:
                self.to_remove = True
        else:
            self.to_remove = True


# ======================================================================


class Info_about_unit(Base_window):
    def __init__(self, id, dict_with_units):
        # basic variables
        self.to_remove = False
        # basic data about unit
        self.id = id  
        self.name = dict_with_units[id].name
        self.base_HP = dict_with_units[id].base_HP
        self.player_id = dict_with_units[id].player_id
        self.team_id = dict_with_units[id].team_id
        # variables for managing the graphics window
        window_height = 100
        self.window_rect = pygame.Rect(10, WIN_HEIGHT - window_height - 10, 300, window_height)
        # fonts
        self.font_arial_20 = pygame.font.SysFont('arial', 20)
        self.name_text = self.font_arial_20.render(self.name, True, LIME)
        self.id_text = self.font_arial_20.render("#" + str(self.id), True, GRAY)

    def draw(self, win, dict_with_units):
    # draw windows with unit's infos and controls
        if self.id in dict_with_units:
            if dict_with_units[self.id].is_selected:
                # background
                pygame.draw.rect(win, BLACK, self.window_rect)
                # lines of title bar
                pygame.draw.line(win, LIME, self.window_rect.bottomleft, self.window_rect.topleft, 3) # left
                pygame.draw.line(win, LIME, self.window_rect.topleft, self.window_rect.topright, 3) # top
                pygame.draw.line(win, LIME, self.window_rect.topright, self.window_rect.bottomright, 3) # right
                pygame.draw.line(win, LIME, self.window_rect.bottomright, self.window_rect.bottomleft, 3) # bottom
                # player circle
                pygame.draw.circle(win, player_color(self.player_id), [self.window_rect.topleft[0] + 18, self.window_rect.topleft[1] + 21], 8, 0)
                # infos about unit
                win.blit(self.name_text, [self.window_rect.topleft[0] + 30, self.window_rect.topleft[1] + 10])
                if dict_with_units[self.id].is_alive:
                    percentage_of_HP = dict_with_units[self.id].HP / self.base_HP
                    if percentage_of_HP > 0.5: color = LIME
                    elif percentage_of_HP > 0.25: color = YELLOW
                    else: color = RED
                    HP_text = self.font_arial_20.render("HP: " + str(dict_with_units[self.id].HP) + " / " + str(self.base_HP), True, color)          
                else:
                    HP_text = self.font_arial_20.render("Unit is dead", True, GRAY)  
                win.blit(HP_text, [self.window_rect.topleft[0] + 10, self.window_rect.topleft[1] + 30])
                win.blit(self.id_text, [self.window_rect.topleft[0] + 10, self.window_rect.topleft[1] + 50])
            else:
                self.to_remove = True
        else:
            self.to_remove = True

    # def press_left(self, *args):
    # # handle actions after left button is pressed
    #     pass

    # def press_right(self, *args):
    # # handle actions after right button is pressed
    #     pass

# ======================================================================


class Base_slide_button(Base_window):
    path = BUTTON_1_PATH

    def __init__(self, screen_coord, world_coord):
    # initialization of the object

        # basic variables
        self.screen_coord = screen_coord
        self.world_coord = world_coord
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

    def draw(self, win, dict_with_unit):
    # draw the object on the screen
        new_rect = self.sprite.get_rect(center = self.screen_coord)
        win.blit(self.sprite, new_rect.topleft)

    # def press_left(self, *args):
    # # handle actions after left button is pressed
    #     pass

    def press_right(self, dict_with_units, press_coord, is_ctrl_down):
    # handle actions after right button is pressed
        # check if center is pressed
        dist = math.hypot(self.screen_coord[0]-press_coord[0], self.screen_coord[1]-press_coord[1])
        if dist < 25:
            # print("center")
            set_new_target_move(dict_with_units, self.world_coord, is_ctrl_down)
        else:
            # check sector       
            angle = math.degrees(angle_to_target(self.screen_coord, press_coord))
            if angle < 270 and angle > 90:
                # print("left")
                set_new_target_regroup(dict_with_units, self.world_coord, is_ctrl_down)
            else:
                # print("right")
                set_new_target_move(dict_with_units, self.world_coord, is_ctrl_down)
        print()
        self.to_remove = True
