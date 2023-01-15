import pygame
import os


def prepare_colors(color):
# prepare list with colors of each team for every pixel
# teams:
# 0 - white
# 1 - blue
# 2 - green
# 3 - red
# 4 - dead unit

    r = color[0]
    g = color[1]
    b = color[2]
    a = color[3]
    
    if r == 255 and g == 0 and b == 0: # full red
        return [(0, 0, 0, a) for _ in range(5)]
    elif r == 237 and g == 28 and b == 36: # red paint
        return [(0, 0, 0, a) for _ in range(5)]
    elif r == 112 and g == 146 and b == 190: # light blue
        return [(205, 205, 205, a),
                color,
                (146, 190, 112, a),
                (190, 112, 146, a),
                (70, 70, 70, a)]
    elif r == 63 and g == 72 and b == 204: # blue
        return [(135, 135, 135, a),
                color,
                (62, 160, 72, a),
                (190, 43, 40, a),
                (50, 50, 50, a)]
    else:
        return [color for _ in range(5)]


def make_teams_sprites(input_folder, output_folder, name_of_file):
# prepare new sprite with units in colors of each team
    number_of_teams = 4 + 1

    # load the file and get basic data about it
    inpot_sprite = pygame.image.load(os.path.join(input_folder, name_of_file))
    input_rect = inpot_sprite.get_rect()
    inpot_sprite_width = input_rect.width
    inpot_sprite_height = input_rect.height

    # make new surface
    output_sprite = pygame.Surface([inpot_sprite_width, inpot_sprite_height * number_of_teams])

    # copy point after point from input image to output image
    for x in range(inpot_sprite_width):
        for y in range(inpot_sprite_height):
            color = inpot_sprite.get_at((x, y))
            list_with_colors = prepare_colors(color)
            for t in range(number_of_teams):
                output_sprite.set_at((x, y + inpot_sprite_height * t), list_with_colors[t])

    # save new file
    pygame.image.save(output_sprite, os.path.join(output_folder, name_of_file))


def make_teams_sprites_from_folder(folder_name, new_folder_name):
# prepare new sprites for all files in folder
    dir_list = os.listdir(folder_name)
    for file_in_dir_list in dir_list:
        make_teams_sprites(folder_name, new_folder_name, file_in_dir_list)

    
if __name__ == "__main__":
    make_teams_sprites_from_folder("input_imgs", "input_imgs")