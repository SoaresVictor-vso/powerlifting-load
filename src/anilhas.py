from . import colors 
import pygame



class Anilha:
    def __init__(self, peso):
        self.peso = peso
        self.color = Anilha.getColor(peso)
        if not self.color:
            raise ValueError(f"Peso inválido para anilha: {peso} kg")

    def __repr__(self):
        return f"Anilha(peso={self.peso}, cor={self.color})"
    
    @staticmethod
    def getColor(weight: float) -> tuple[int, int, int]:
        switcher = {
            25: colors.RED,
            20: colors.BLUE,
            15: colors.YELLOW,
            10: colors.GREEN,
            5: colors.WHITE,
            2.5: colors.DARK_GRAY,
            1.25: colors.DARK_GRAY,
            0.5: colors.DARK_GRAY,
            0.25: colors.DARK_GRAY
        }
        return switcher.get(weight, None)

    def getSize(self) -> tuple[float, float]:
        """
        Returns the (width, height) size of the anilha based on its weight.
        """
        size_map = {
            25: ( 6, 90,),
            20: ( 6, 90,),
            15: ( 6, 90,),
            10: ( 6, 72,),
            5: ( 6, 52,),
            2.5: ( 6, 26,),
            1.25: ( 6, 13,),
            0.5: ( 6, 10,),
            0.25: ( 6, 8)
        }
        return size_map.get(self.peso, (0, 0))

    def draw(self, surface, position: tuple[int, int]) -> None:
        """
        Draw a rectangle in this anilha's color onto a pygame surface.
        Add a black border around the rectangle.
        """
        size_x, size_y = self.getSize()
        rect = pygame.Rect(position[0], position[1] - size_y // 2, size_x, size_y)
        pygame.draw.rect(surface, (0, 0, 0), rect)  # Draw black border
        inner_rect = rect.inflate(-2, -2)  # Shrink rect for inner color
        pygame.draw.rect(surface, self.color, inner_rect)
        # size_x, size_y = self.getSize()
        # rect = pygame.Rect(position[0] , position[1] - size_y // 2, size_x, size_y)
        # pygame.draw.rect(surface, self.color, rect )

    
__all__ = [
    "Anilha",
]