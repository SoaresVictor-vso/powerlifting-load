import pygame
import sys
import random
from src import colors
from src.anilhas import Anilha

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60





# Global list for selected weights
pesos_selecionados = []
peso_sorteado = None
barra_pronta = False
jogo_iniciado = False

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=colors.WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, screen, font):
        # Draw button
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, colors.BLACK, self.rect, 2, border_radius=10)
        
        # Draw text with scaling to fit
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Scale text if it's too wide for the button
        if text_surface.get_width() > self.rect.width - 10:
            scale_factor = (self.rect.width - 10) / text_surface.get_width()
            new_width = int(text_surface.get_width() * scale_factor)
            new_height = int(text_surface.get_height() * scale_factor)
            text_surface = pygame.transform.scale(text_surface, (new_width, new_height))
            text_rect = text_surface.get_rect(center=self.rect.center)
        
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]

# Button class for weight plates
class BotaoPeso:
    def __init__(self, x, y, width, height, peso: float):
        self.rect = pygame.Rect(x, y, width, height)
        self.peso = peso
        self.color = Anilha.getColor(peso)
        self.hover_color = colors.DARK_GRAY
        self.is_hovered = False
        
    def draw(self, screen, font):
        # Draw button
               
        if (not self.can_click()):
            color = colors.GRAY
        else:
            color = self.hover_color if self.is_hovered else self.color

        if color == colors.WHITE or color == colors.YELLOW:
            font_color = colors.BLACK
        else:
            font_color = colors.WHITE

        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, colors.BLACK, self.rect, 2, border_radius=10)
        
        # Draw text
        text = f"{self.peso}kg"
        text_surface = font.render(text, True, font_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_pressed):
        if not self.can_click():
            return False
        if self.rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            global pesos_selecionados
            pesos_selecionados.append(self.peso)
            return True
        return False
    
    def can_click(self):
        return not any(x < self.peso for x in pesos_selecionados)
        
    
class Presilha:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.color = colors.GRAY

    def draw(self, surface, position: tuple[int, int]) -> None:
        rect = pygame.Rect(position[0], position[1] - self.height // 2, self.width, self.height)
        pygame.draw.rect(surface, colors.BLACK, rect)  # Draw black border
        inner_rect = rect.inflate(-2, -2)  # Shrink rect for inner color
        pygame.draw.rect(surface, self.color, inner_rect)




def main():
    global peso_sorteado, jogo_iniciado, barra_pronta, pesos_selecionados
    
    # Setup display
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Counter Game")
    clock = pygame.time.Clock()
    
    # Fonts
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 36)
    

    
    # Track mouse button state to prevent multiple increments
    mouse_was_pressed = False

    PESOS_POSSIVEIS = [25, 20, 15, 10, 5, 2.5, 1.25, 0.5, 0.25]

    def get_anilhas_corretas(peso: float) -> list[float]:
        BARRA = 20
        PRESILHA = 2.5
        total_lateral = ((peso - BARRA) / 2 )- PRESILHA
        total_restante = total_lateral
        pesos = []
    
    

        for weight in PESOS_POSSIVEIS:
            while total_restante >= weight:
                pesos.append(weight)
                total_restante -= weight   

        return pesos 
    
    def get_peso_total(anilhas: list[float]) -> float:
        BARRA = 20
        PRESILHA = 2.5
        return BARRA + PRESILHA * 2 + sum(anilhas) * 2
        

    

    # Create buttons for each weight using BotaoPeso
    weight_buttons = []
    button_x = 50
    button_y = 500
    button_width = 80
    button_height = 40
    button_spacing = 10

    for i, peso in enumerate(PESOS_POSSIVEIS):
        if i == 5:
            button_x = 50
            button_y += button_height + button_spacing

        weight_buttons.append(BotaoPeso(
            x=button_x,
            y=button_y,
            width=button_width,
            height=button_height,
            peso=peso
        ))
        button_x += button_width + button_spacing
    
    # Create "Iniciar" button
    start_button = Button(
        x=WINDOW_WIDTH // 2 - 60,
        y=20,
        width=120,
        height=50,
        text="Iniciar",
        color=colors.GREEN,
        hover_color=colors.DARK_GREEN
    )
    
    # Create "Barra Pronta" button
    barra_pronta_button = Button(
        x=WINDOW_WIDTH - 160,
        y=20,
        width=140,
        height=50,
        text="Barra Pronta",
        color=colors.BLUE,
        hover_color=colors.DARK_BLUE
    )
    
    # Create "Limpar" button
    limpar_button = Button(
        x=WINDOW_WIDTH - 160,
        y=80,
        width=140,
        height=50,
        text="Limpar",
        color=colors.RED,
        hover_color=colors.DARK_GRAY
    )
    
    # Create "Mostrar Correta" button
    mostrar_correta_button = Button(
        x=WINDOW_WIDTH - 160,
        y=140,
        width=140,
        height=50,
        text="Mostrar Correta",
        color=colors.YELLOW,
        hover_color=colors.DARK_GRAY,
        text_color=colors.BLACK
        
    )
    
    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Get mouse state
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        # Update start button hover state and check for clicks
        if not jogo_iniciado:
            start_button.check_hover(mouse_pos)
            if start_button.is_clicked(mouse_pos, mouse_pressed) and not mouse_was_pressed:
                # Generate random weight (multiple of 0.5) between 25 and 500
                peso_sorteado = round(random.uniform(25, 500) * 2) / 2
                jogo_iniciado = True
                pesos_selecionados = []
        
        # Update barra pronta button hover state and check for clicks
        if jogo_iniciado and not barra_pronta:
            barra_pronta_button.check_hover(mouse_pos)
            if barra_pronta_button.is_clicked(mouse_pos, mouse_pressed) and not mouse_was_pressed:
                barra_pronta = True
        
        # Update limpar button hover state and check for clicks
        if barra_pronta:
            limpar_button.check_hover(mouse_pos)
            if limpar_button.is_clicked(mouse_pos, mouse_pressed) and not mouse_was_pressed:
                # Reset game state
                peso_sorteado = None
                jogo_iniciado = False
                barra_pronta = False
                pesos_selecionados = []
        
        # Update mostrar correta button hover state and check for clicks
        if barra_pronta and peso_sorteado is not None:
            peso_total = get_peso_total(pesos_selecionados)
            anilhas_corretas = get_anilhas_corretas(peso_sorteado)
            acertou = anilhas_corretas == pesos_selecionados
            
            if not acertou:
                mostrar_correta_button.check_hover(mouse_pos)
                if mostrar_correta_button.is_clicked(mouse_pos, mouse_pressed) and not mouse_was_pressed:
                    pesos_selecionados = get_anilhas_corretas(peso_sorteado)
        
        # Update weight buttons hover state and check for clicks
        for weight_button in weight_buttons:
            weight_button.check_hover(mouse_pos)
            if mouse_pressed[0] and not mouse_was_pressed:
                weight_button.is_clicked(mouse_pos, mouse_pressed)
        
        
        bar_center_x = WINDOW_WIDTH // 2
        bar_center_y = WINDOW_HEIGHT // 2

        mouse_was_pressed = mouse_pressed[0]
        
        # Drawing
        screen.fill(colors.GRAY)
        
        # Draw appropriate buttons based on game state
        if not jogo_iniciado:
            start_button.draw(screen, font_small)
        elif not barra_pronta:
            barra_pronta_button.draw(screen, font_small)
        else:
            limpar_button.draw(screen, font_small)
            # Show "Mostrar Correta" button if user got it wrong
            if peso_sorteado is not None:
                peso_total = get_peso_total(pesos_selecionados)
                anilhas_corretas = get_anilhas_corretas(peso_sorteado)
                acertou = anilhas_corretas == pesos_selecionados
                if not acertou:
                    mostrar_correta_button.draw(screen, font_small)
        
        # Draw weight label if a weight has been generated
        if peso_sorteado is not None and not barra_pronta:
            label_text = f"Carregar com {peso_sorteado}kg"
            label_surface = font_medium.render(label_text, True, colors.BLACK)
            label_rect = label_surface.get_rect(center=(WINDOW_WIDTH // 2, 50))
            screen.blit(label_surface, label_rect)
        
        # Show result when barra pronta is clicked
        if barra_pronta and peso_sorteado is not None:
            peso_total = get_peso_total(pesos_selecionados)
            anilhas_corretas = get_anilhas_corretas(peso_sorteado)
            acertou = anilhas_corretas == pesos_selecionados
            
            # Draw target weight
            target_text = f"Objetivo: {peso_sorteado}kg"
            target_surface = font_medium.render(target_text, True, colors.BLACK)
            target_rect = target_surface.get_rect(center=(WINDOW_WIDTH // 2, 50))
            screen.blit(target_surface, target_rect)
            
            # Draw actual weight
            actual_text = f"Peso Total: {peso_total}kg"
            actual_surface = font_medium.render(actual_text, True, colors.BLACK)
            actual_rect = actual_surface.get_rect(center=(WINDOW_WIDTH // 2, 100))
            screen.blit(actual_surface, actual_rect)
            
            # Draw three circles to indicate result
            circle_radius = 25
            circle_spacing = 70
            center_x = WINDOW_WIDTH // 2
            circle_y = 160
            
            circle_color = colors.WHITE if acertou else colors.RED
            
            for i in range(3):
                circle_x = center_x - circle_spacing + (i * circle_spacing)
                pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)
                pygame.draw.circle(screen, colors.BLACK, (circle_x, circle_y), circle_radius, 3)
        
        # Draw weight buttons
        for weight_button in weight_buttons:
            weight_button.draw(screen, font_small)
        
        # Draw list of selected weights on the left side
        if len(pesos_selecionados) > 0:
            # Count occurrences of each weight
            peso_counts = {}
            for peso in pesos_selecionados:
                peso_counts[peso] = peso_counts.get(peso, 0) + 1
            
            # Draw title
            list_title = "Anilhas:"
            title_surface = font_small.render(list_title, True, colors.BLACK)
            screen.blit(title_surface, (20, 100))
            
            # Draw each weight with its count
            y_offset = 140
            for peso, count in sorted(peso_counts.items(), reverse=True):
                text = f"{peso}kg ({count})"
                text_surface = font_small.render(text, True, colors.BLACK)
                screen.blit(text_surface, (20, y_offset))
                y_offset += 35

            if barra_pronta:
                text = f"Presilha: 2.5kg (1)"
                text_surface = font_small.render(text, True, colors.BLACK)
                screen.blit(text_surface, (20, y_offset))

        # Draw bar
        bar_length = 450
        bar_thickness = 7
        bar_rect = pygame.Rect(bar_center_x - bar_length // 2, bar_center_y - bar_thickness // 2, bar_length, bar_thickness)
        pygame.draw.rect(screen, colors.DARK_GRAY, bar_rect, border_radius=8)
        pygame.draw.rect(screen, colors.BLACK, bar_rect, 2, border_radius=8)

        # Draw collars (small sleeves next to the center)
        collar_w, collar_h = 10, 20
        collar_offset = 150
        left_collar_x = bar_center_x - collar_offset - collar_w
        right_collar_x = bar_center_x + collar_offset
        left_collar = pygame.Rect(left_collar_x, bar_center_y - collar_h // 2, collar_w, collar_h)
        right_collar = pygame.Rect(right_collar_x, bar_center_y - collar_h // 2, collar_w, collar_h)
        pygame.draw.rect(screen, colors.BLACK, left_collar, border_radius=4)
        pygame.draw.rect(screen, colors.BLACK, right_collar, border_radius=4)
        pygame.draw.rect(screen, colors.GRAY, left_collar.inflate(-6, -6), border_radius=3)
        pygame.draw.rect(screen, colors.GRAY, right_collar.inflate(-6, -6), border_radius=3)

        # Draw plates (anilhas) on both sides, spaced outward from the collars
        print( pesos_selecionados)
        offset = -2
        for i, peso in enumerate(pesos_selecionados):
            offset += 6
            plate = Anilha(peso)
            plate.draw(screen, position=(-1 * offset + left_collar_x, bar_center_y))
            plate.draw(screen, position=(offset + right_collar_x + collar_w // 2, bar_center_y))

        if barra_pronta:
            presilha = Presilha()
            presilha.draw(screen, position=(left_collar_x - presilha.width - offset , bar_center_y))
            presilha.draw(screen, position=(right_collar_x + collar_w + offset, bar_center_y))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
