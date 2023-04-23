import pygame

# from settings import *
from setup import *
from settings import *
from classes_units import *
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
    # return True if pressed and False if not
        return False

    def press_right(self, *args):
    # handle actions after right button is pressed
    # return True if pressed and False if not
        return False


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
        window_height = 190
        window_width = 330
        self.window_rect = pygame.Rect(10, WIN_HEIGHT - window_height - 10, window_width, window_height)
        # fonts
        self.font_arial_20 = pygame.font.SysFont('arial', 20)
        self.font_arial_15 = pygame.font.SysFont('arial', 15)
        # fixed textes
        self.name_text = self.font_arial_20.render(self.name, True, LIME)
        self.id_text = self.font_arial_20.render("#" + str(self.id), True, GRAY)
        self.price_text = self.font_arial_15.render("Cost:  " + str(dict_with_units[id].price), True, GRAY)
        self.speed_text = self.font_arial_15.render("Speed:  " + str(dict_with_units[id].v_max), True, GRAY)
        self.weapons_data_texts = [self.font_arial_15.render("Weapons:", True, GRAY)]
        for weapon in dict_with_units[id].Weapons:
            self.weapons_data_texts.append(self.font_arial_15.render("-" + weapon.description, True, GRAY))

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
                # unit icon
                # pygame.draw.circle(win, player_color(self.player_id), [self.window_rect.topleft[0] + 18, self.window_rect.topleft[1] + 21], 8, 0)
                coord_on_screen = [self.window_rect.left + 18, self.window_rect.top + 21]
                dict_with_units[self.id].draw_level_indicator(win, coord_on_screen)
                dict_with_units[self.id].draw_unit_type_icon(win, coord_on_screen)
                dict_with_units[self.id].draw_unit_application_icon(win, coord_on_screen)
                # infos about unit
                # column I
                win.blit(self.name_text, [self.window_rect.left + 30, self.window_rect.top + 10])
                if dict_with_units[self.id].is_alive:
                    percentage_of_HP = dict_with_units[self.id].HP / self.base_HP
                    if percentage_of_HP > 0.5: color = LIME
                    elif percentage_of_HP > 0.25: color = YELLOW
                    else: color = RED
                    HP_text = self.font_arial_20.render("HP: " + str(dict_with_units[self.id].HP) + " / " + str(self.base_HP), True, color)          
                else:
                    HP_text = self.font_arial_20.render("Unit is dead", True, GRAY)  
                win.blit(HP_text, [self.window_rect.left + 10, self.window_rect.top + 30])
                win.blit(self.id_text, [self.window_rect.left + 10, self.window_rect.top + 50])
                win.blit(self.price_text, [self.window_rect.left + 10, self.window_rect.top + 80])
                win.blit(self.speed_text, [self.window_rect.left + 10, self.window_rect.top + 95])
                # column II
                i = 0
                for weapon_data_text in self.weapons_data_texts:
                    win.blit(weapon_data_text, [self.window_rect.left + 170, self.window_rect.top + 10 + 15*i])
                    i += 1

            else:
                self.to_remove = True
        else:
            self.to_remove = True


# ======================================================================


class Shop_unit_label: #(Base_window):
    def __init__(self, id, unit, origin, extra_wide=False):
        self.id = id
        # basic data about unit
        self.Unit = unit 
        self.name = unit.name
        self.price = unit.price
        self.base_HP = unit.base_HP
        self.player_id = unit.player_id
        self.team_id = unit.team_id
        # variables for managing the graphics window
        self.extra_wide = extra_wide
        self.origin = origin
        window_height = 190
        if extra_wide: window_width = 300
        else: window_width = 200
        self.window_rect = pygame.Rect(*origin, window_width, window_height)
        # fonts
        self.font_arial_20 = pygame.font.SysFont('arial', 20)
        self.font_arial_15 = pygame.font.SysFont('arial', 15)
        # fixed textes
        self.name_text = self.font_arial_20.render(self.name, True, LIME)
        self.price_text = self.font_arial_15.render("Cost:  " + str(unit.price), True, GRAY)
        self.HP_text = self.font_arial_15.render("HP:  " + str(unit.base_HP), True, GRAY)
        self.speed_text = self.font_arial_15.render("Speed:  " + str(unit.v_max), True, GRAY)
        self.weapons_data_texts = [self.font_arial_15.render("Weapons:", True, GRAY)]
        for weapon in unit.Weapons:
            self.weapons_data_texts.append(self.font_arial_15.render("-" + weapon.description, True, GRAY))

    def draw(self, win):
    # draw windows with unit's infos and prices

        # lines of title bar
        pygame.draw.line(win, LIME, (self.window_rect.right, self.window_rect.top + 20), \
                         (self.window_rect.right, self.window_rect.bottom - 20), 3) # right
        # unit icon
        coord_on_screen = [self.window_rect.left + 18, self.window_rect.top + 21]
        self.Unit.draw_level_indicator(win, coord_on_screen)
        self.Unit.draw_unit_type_icon(win, coord_on_screen)
        self.Unit.draw_unit_application_icon(win, coord_on_screen)
        # infos about unit
        # column I
        win.blit(self.name_text, [self.window_rect.left + 30, self.window_rect.top + 10])
        win.blit(self.price_text, [self.window_rect.left + 10, self.window_rect.top + 35])
        win.blit(self.HP_text, [self.window_rect.left + 10, self.window_rect.top + 50])
        win.blit(self.speed_text, [self.window_rect.left + 10, self.window_rect.top + 65])
        # column II
        i = 0
        for weapon_data_text in self.weapons_data_texts:
            if self.extra_wide:
                win.blit(weapon_data_text, [self.window_rect.left + 130, self.window_rect.top + 10 + 15*i])
            else:
                win.blit(weapon_data_text, [self.window_rect.left + 10, self.window_rect.top + 85 + 15*i])
            i += 1

    def press_left(self, dict_with_units, press_coord):
    # handle actions after left button is pressed
        if self.window_rect.collidepoint(press_coord): 
            dict_with_units[self.id].add_unit_to_queue(self.Unit)


# ======================================================================


class Base_page:
    name = "temp"
    def __init__(self, id, dict_with_units, lvl_of_page, number_of_page):
    # initialization of the object

        # basic variables
        self.id = id
        self.is_active = False

        # variables for managing the graphics window
        # horizontally
        margin = 300
        title_width = 100
        # vertically
        origin_vert_pos = WIN_HEIGHT - 375      
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


class Page_with_shop(Base_page):
    name = "temp shop"
    Product_classes = [Light_tank, Light_tank]
    extra_wide = False

    def __init__(self, id, dict_with_units, lvl_of_page, number_of_page):
        Base_page.__init__(self, id, dict_with_units, lvl_of_page, number_of_page)

        coord = dict_with_units[id].coord
        angle = dict_with_units[id].angle
        player_id = dict_with_units[id].player_id
        team_id = dict_with_units[id].team_id

        self.list_with_products = []
        if self.extra_wide: product_width = 300
        else: product_width = 200
        i = 0
        for product in self.Product_classes:
            origin = (self.page_rect.left + i * product_width, self.page_rect.top)
            self.list_with_products.append(Shop_unit_label(id, product(0, coord, angle, player_id, team_id), origin, self.extra_wide))
            i += 1

    def draw(self, win):
    # draw the object on the screen 
        Base_page.draw(self, win)
        if self.is_active:
            for product in self.list_with_products:
                product.draw(win)

    def press_left(self, dict_with_units, press_coord):
    # handle actions after left button is pressed
        if self.is_active:
            for product in self.list_with_products:
                product.press_left(dict_with_units, press_coord)

class Page_land_T1(Page_with_shop):
    name = "T1"
    Product_classes = [Space_marine, Light_tank]

class Page_land_T2(Page_with_shop):
    name = "T2"
    Product_classes = [Super_space_marine, Main_battle_tank, Spider_tank]

class Page_land_T3(Page_with_shop):
    name = "T3"
    Product_classes = [Heavy_tank, Heavy_artillery]

class Page_air_T1(Page_with_shop):
    name = "T1"
    Product_classes = []

class Page_air_T2(Page_with_shop):
    name = "T2"
    Product_classes = [Fighter, Bomber]

class Page_air_T3(Page_with_shop):
    name = "T3"
    Product_classes = [Strategic_bomber]

class Page_navy_T1(Page_with_shop):
    name = "T1"
    Product_classes = [Small_artillery_ship, Small_AA_ship]

class Page_navy_T2(Page_with_shop):
    name = "T2"
    Product_classes = [Battle_cruiser]

class Page_navy_T3(Page_with_shop):
    name = "T3"
    Product_classes = [Destroyer, Battleship]
    extra_wide = True

class Page_factory(Page_with_shop):
    name = "Upgrade"
    Product_classes = []


class Page_with_notebook(Base_page):
    name = "temp note"
    Page_classes = [Base_page, Base_page]

    def __init__(self, id, dict_with_units, lvl_of_page, number_of_page):
        Base_page.__init__(self, id, dict_with_units, lvl_of_page, number_of_page)

        # initialization of tabs
        self.list_with_pages = []
        number_of_page = 0
        for page_class in self.Page_classes:
            self.list_with_pages.append(page_class(id, dict_with_units, lvl_of_page + 1, number_of_page))
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


class Page_land(Page_with_notebook):
    name = "Land"
    Page_classes = [Page_land_T1, Page_land_T2, Page_land_T3]

class Page_air(Page_with_notebook):
    name = "Air"
    Page_classes = [Page_air_T2, Page_air_T3] # Page_air_T1, 

class Page_navy(Page_with_notebook):
    name = "Navy"
    Page_classes = [Page_navy_T1, Page_navy_T2, Page_navy_T3]

# ======================================================================


class Base_notebook:
    Page_classes = [Base_page, Page_with_notebook, Base_page]

    def __init__(self, id, dict_with_units):
    # initialization of the object

        # basic variables
        self.id = id
        self.to_remove = False

        # initialization of tabs
        self.list_with_pages = []
        number_of_page = 0
        for page_class in self.Page_classes:
            self.list_with_pages.append(page_class(id, dict_with_units, 0, number_of_page))
            number_of_page += 1
        self.list_with_pages[0].is_active = True

    def draw(self, win, dict_with_units):
    # draw the object on the screen
        if self.id in dict_with_units:
            if dict_with_units[self.id].is_selected:
                for page in self.list_with_pages:
                    page.draw(win)
            else:
                self.to_remove = True
        else:
            self.to_remove = True

    def press_left(self, list_with_units, press_coord):
    # handle actions after left button is pressed
    # return True if pressed and False if not

        # check if the notebook has been pressed at all:
        was_pressed = False
        for page in self.list_with_pages:
            if page.is_active:
                if page.is_title_pressed(press_coord): # title of active tab is pressed
                    was_pressed = True
                elif page.is_page_pressed(press_coord): # page (body) is pressed
                    was_pressed = True
            else:
                if page.is_title_pressed(press_coord): # title of inactive tab is pressed
                    was_pressed = True
        # if the notebook has been pressed do the action:
        if was_pressed:
            for page in self.list_with_pages:
                if page.is_active:
                    if page.is_title_pressed(press_coord): # title of active tab is pressed
                        pass
                    elif page.is_page_pressed(press_coord): # page (body) is pressed
                        page.press_left(list_with_units, press_coord)
                    else: # nothing on this tab has been pressed
                        page.is_active = False
                else:
                    if page.is_title_pressed(press_coord): # title of inactive tab is pressed
                        page.is_active = True
            return True
        # if not pressed return False
        else: return False

    def press_right(self, *args):
    # handle actions after right button is pressed
    # return True if pressed and False if not
        return False


class Notebook_universal_factory(Base_notebook):
    Page_classes = [Page_land, Page_air, Page_navy, Page_factory]

class Notebook_land_factory(Base_notebook):
    Page_classes = [Page_land, Page_air, Page_factory]

class Notebook_navy_factory(Base_notebook):
    Page_classes = [Page_navy, Page_factory]


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

        # pause button
        self.pause_button_rect = pygame.Rect(origin_horz_pos - 2*self.field_size, origin_vert_pos, self.field_size, self.field_size)
        # loop button
        self.loop_button_rect = pygame.Rect(origin_horz_pos - self.field_size, origin_vert_pos, self.field_size, self.field_size)
        # load and prepare sprite
        self.sprite_loop = pygame.image.load(os.path.join(*BUTTON_4_PATH))
        self.sprite_loop.convert()
        self.sprite_loop.set_colorkey(BLACK)
        self.sprite_pause = pygame.image.load(os.path.join(*BUTTON_5_PATH))
        self.sprite_pause.convert()
        self.sprite_pause.set_colorkey(BLACK)
        self.sprite_play = pygame.image.load(os.path.join(*BUTTON_6_PATH))
        self.sprite_play.convert()
        self.sprite_play.set_colorkey(BLACK)

    def draw(self, win, dict_with_units):
    # draw windows with unit's queue
        if self.id in dict_with_units:
            if dict_with_units[self.id].is_selected:
            # draw pause button
                # background and icon
                if dict_with_units[self.id].production_is_on:
                    pygame.draw.rect(win, BLACK, self.pause_button_rect)
                    win.blit(self.sprite_play, self.pause_button_rect.topleft)
                else: 
                    if len(dict_with_units[self.id].list_building_queue): # when queue is not empty
                        pygame.draw.rect(win, GRAY, self.pause_button_rect)
                    else:
                        pygame.draw.rect(win, BLACK, self.pause_button_rect)
                    win.blit(self.sprite_pause, self.pause_button_rect.topleft)
                # lines
                pygame.draw.line(win, LIME, self.pause_button_rect.topright, self.pause_button_rect.topleft, 3) # top
                pygame.draw.line(win, LIME, self.pause_button_rect.topleft, self.pause_button_rect.bottomleft, 3) # left
                pygame.draw.line(win, LIME, self.pause_button_rect.bottomleft, self.pause_button_rect.bottomright, 3) # bottom

            # draw loop button
                # background
                if dict_with_units[self.id].loop_mode_is_on:
                    pygame.draw.rect(win, GRAY, self.loop_button_rect)
                else: 
                    pygame.draw.rect(win, BLACK, self.loop_button_rect)
                # lines
                pygame.draw.line(win, LIME, self.loop_button_rect.topright, self.loop_button_rect.topleft, 3) # top
                pygame.draw.line(win, LIME, self.loop_button_rect.topleft, self.loop_button_rect.bottomleft, 3) # left
                pygame.draw.line(win, LIME, self.loop_button_rect.bottomleft, self.loop_button_rect.bottomright, 3) # bottom
                # icon
                win.blit(self.sprite_loop, self.loop_button_rect.topleft)

            # draw queue bar
                # background
                pygame.draw.rect(win, BLACK, self.window_rect)
                # lines of title bar
                pygame.draw.line(win, LIME, self.window_rect.topleft, self.window_rect.topright, 3) # top
                pygame.draw.line(win, LIME, self.window_rect.bottomright, self.window_rect.bottomleft, 3) # bottom
                origin = self.window_rect.topleft
                for i in range(self.queue_slots + 1):         
                    pygame.draw.line(win, LIME, (origin[0] + i * self.field_size, origin[1]), (origin[0] + i * self.field_size, origin[1] + self.field_size), 3)  

                # draw queue
                len_of_queue = len(dict_with_units[self.id].list_building_queue)
                for no_of_slot in range(len_of_queue):
                    coord_on_screen = [self.window_rect.left + no_of_slot * self.field_size + self.field_size // 2, self.window_rect.center[1]]
                    dict_with_units[self.id].list_building_queue[no_of_slot].draw_level_indicator(win, coord_on_screen)
                    dict_with_units[self.id].list_building_queue[no_of_slot].draw_unit_type_icon(win, coord_on_screen)
                    dict_with_units[self.id].list_building_queue[no_of_slot].draw_unit_application_icon(win, coord_on_screen)

            # draw progress
                pygame.draw.line(win, BLUE, 
                            [self.window_rect.left, self.window_rect.bottom + 10],
                            [self.window_rect.left + self.window_rect.width * dict_with_units[self.id].BP / dict_with_units[self.id].base_BP, self.window_rect.bottom + 10], 5)

            else:
                self.to_remove = True
        else:
            self.to_remove = True

    def press_left(self, dict_with_units, press_coord):
    # handle actions after left button is pressed
    # return True if pressed and False if not
        if self.window_rect.collidepoint(press_coord): 
            no_of_slot = (press_coord[0] - self.window_rect.left) // self.field_size
            dict_with_units[self.id].remove_unit_from_queue(no_of_slot)
            return True
        # loop button
        elif self.loop_button_rect.collidepoint(press_coord):
            if dict_with_units[self.id].loop_mode_is_on: 
                dict_with_units[self.id].loop_mode_is_on = False
            else:
                dict_with_units[self.id].loop_mode_is_on = True
            return True
        # pause button
        elif self.pause_button_rect.collidepoint(press_coord):
            if dict_with_units[self.id].production_is_on: 
                dict_with_units[self.id].production_is_on = False
            else:
                if len(dict_with_units[self.id].list_building_queue): # when queue is not empty
                    dict_with_units[self.id].production_is_on = True
            return True
        else: return False


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

    def press_right(self, map, dict_with_units, press_coord, is_ctrl_down):
    # handle actions after right button is pressed
        # check if center is pressed
        dist = math.hypot(self.screen_coord[0]-press_coord[0], self.screen_coord[1]-press_coord[1])
        if dist < 25:
            # print("center")
            set_new_target_move(map, dict_with_units, self.world_coord, is_ctrl_down)
        else:
            # check sector       
            angle = math.degrees(angle_to_target(self.screen_coord, press_coord))
            if angle < 270 and angle > 90:
                # print("left")
                set_new_target_regroup(map, dict_with_units, self.world_coord, is_ctrl_down)
            else:
                # print("right")
                set_new_target_move(map, dict_with_units, self.world_coord, is_ctrl_down)
        # print()
        self.to_remove = True
    # return True if pressed and False if not
        return False
    

class Slide_button_with_cancel(Base_slide_button):
    path = BUTTON_2_PATH

    def press_right(self, map, dict_with_units, press_coord, is_ctrl_down):
    # handle actions after right button is pressed
        # check if center is pressed
        dist = math.hypot(self.screen_coord[0]-press_coord[0], self.screen_coord[1]-press_coord[1])
        if dist < 25:
            # print("center")
            set_new_target_move(map, dict_with_units, self.world_coord, is_ctrl_down)
        else:
            # check sector       
            angle = math.degrees(angle_to_target(self.screen_coord, press_coord))
            if angle < 270 and angle > 120:
                # print("left")
                set_new_target_regroup(map, dict_with_units, self.world_coord, is_ctrl_down)
            elif angle >= 270 or angle < 60:
                # print("right")
                set_new_target_move(map, dict_with_units, self.world_coord, is_ctrl_down)
            else:
                # print("cancel")
                pass
        # print()
        self.to_remove = True
    # return True if pressed and False if not
        return False


class Slide_button_for_factory(Base_slide_button):
    path = BUTTON_3_PATH

    def press_right(self, map, dict_with_units, press_coord, is_ctrl_down):
    # handle actions after right button is pressed
        # check if center is pressed
        dist = math.hypot(self.screen_coord[0]-press_coord[0], self.screen_coord[1]-press_coord[1])
        if dist < 25:
            print("center")
            # set_new_target_move(dict_with_units, self.world_coord, is_ctrl_down)
        else:
            # check sector       
            angle = math.degrees(angle_to_target(self.screen_coord, press_coord))
            if angle < 60 or angle > 120:
                print("outside")
                # set_new_target_regroup(dict_with_units, self.world_coord, is_ctrl_down)
            else:
                print("cancel")
                # pass
        print()
        self.to_remove = True
    # return True if pressed and False if not
        return False