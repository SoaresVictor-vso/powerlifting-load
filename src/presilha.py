import pygame
from src import colors


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

__all__ = ["Presilha"]