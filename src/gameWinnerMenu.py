
import pygame

class GameWinnerMenu:
    def __init__(self, display):
        self.display = display
        self.screen_width, self.screen_height = self.display.get_size()  # Lấy kích thước màn hình

        # Khởi tạo phông chữ
        self.title_font = pygame.font.Font(None, 80)
        self.button_font = pygame.font.Font(None, 40)                
        self.back_button_font = pygame.font.Font(None, 40)  # Tăng kích thước phông chữ nút "Back"
        
        # Tạo nút Restart ở giữa màn hình
        button_width, button_height = 200, 60
        self.restart_button_rect = pygame.Rect(
            (self.screen_width - button_width) // 2, 
            (self.screen_height - button_height) // 2 + 50,  # Đặt hơi thấp hơn chính giữa
            button_width, 
            button_height
        )
        
        # Màu sắc
        self.bg_color = (30, 30, 30)  # Màu nền xám đậm
        self.text_color = (255, 255, 255)  # Màu chữ trắng
        self.button_color = (200, 0, 0)  # Màu nền nút đỏ
        self.button_hover_color = (255, 50, 50)  # Màu nền nút khi hover
        self.button_border_color = (255, 255, 255)  # Màu viền trắng

        # Tạo nút Back là một dòng chữ ở phía dưới màn hình
        self.back_text = self.back_button_font.render("Back", True, (26, 26, 26))  # Dòng chữ "Back"
        self.back_text_rect = self.back_text.get_rect(center=(self.screen_width / 2, self.screen_height - 40))  # Đặt gần dưới cùng màn hình

    def draw(self):
        # Tô màu nền
        for i in range(0, self.display.get_height(), 2):
            color = (30, 30 + i // 5, 60 + i // 10)
            pygame.draw.line(self.display, color, (0, i), (self.display.get_width(), i))
            
        # Hiển thị hình ảnh
        image = pygame.image.load("../graphics/objects/crown/0.png")  # Thay đường dẫn tới ảnh của bạn
        image = pygame.transform.scale(image, (150, 150))  # Thay đổi kích thước ảnh nếu cần
        image_rect = image.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 170))
        self.display.blit(image, image_rect)

        # Hiển thị chữ "Game winner"
        game_over_text = self.title_font.render("Winner", True, self.text_color)
        text_rect = game_over_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 60))
        self.display.blit(game_over_text, text_rect)

        # Hiển thị chữ "Back" (không có viền) gần phía dưới màn hình
        self.display.blit(self.back_text, self.back_text_rect)


    def check_restart_click(self, event):
        # Kiểm tra nếu người dùng nhấn nút Restart
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_button_rect.collidepoint(event.pos):
                return True
        return False

    def check_back_click(self, event):
        # Kiểm tra nếu người dùng nhấn nút Back
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_text_rect.collidepoint(event.pos):
                return True
        return False

    def check_restart_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_button_rect.collidepoint(event.pos):                
                return True
        return False