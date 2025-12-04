import pygame

from src import colors


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
    
__all__ = ["Button"]