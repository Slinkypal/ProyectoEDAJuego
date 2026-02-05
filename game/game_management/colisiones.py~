def check_collision(player_x, player_y, player_w, player_h, sprite_x, sprite_y, sprite_w, sprite_h):
    # Colisiones
    
    # Calcular los bordes del Jugador (suponiendo x,y en el centro)
    p_left = player_x - (player_w // 2)
    p_right = player_x + (player_w // 2)
    p_top = player_y - (player_h // 2)
    p_bottom = player_y + (player_h // 2)

    # Calcular los bordes del Sprite/Objeto (suponiendo x,y en esquina superior izq)
    s_left = sprite_x
    s_right = sprite_x + sprite_w
    s_top = sprite_y
    s_bottom = sprite_y + sprite_h

    # Comprobar superposición (Lógica AABB)
    if (p_right > s_left and 
        p_left < s_right and 
        p_bottom > s_top and 
        p_top < s_bottom):
        return True # ¡Hay colisión!
    
    return False
