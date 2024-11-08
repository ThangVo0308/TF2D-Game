# alert.py
import pygame
import os

class Alert:
    def __init__(self):        
        self.display_surface = pygame.display.get_surface()
        self.show_alert = False
        self.alert_start_time = 0
        self.alert_duration = 2000  # Thời gian hiển thị alert
        self.alert_text = ""  # Thay đổi nội dung theo nhu cầu

    def wrap_text(self, text, font, max_width):
        """Chia đoạn text thành nhiều dòng nếu nó dài hơn max_width."""
        lines = []
        words = text.split(' ')
        current_line = ""

        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] <= max_width:  # Kiểm tra chiều dài
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '  # Bắt đầu dòng mới
        lines.append(current_line)  # Thêm dòng cuối cùng
        return lines

    def get_font(self, size):
        return pygame.font.Font(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 
                                             'graphics', 'font', 'start_menu_font.ttf'), size)        

    def display_alert(self, alert_text, alert_duration=2000):        
        if not self.show_alert:
            self.show_alert = True
            self.alert_text = alert_text
            self.alert_start_time = pygame.time.get_ticks()  # Ghi lại thời gian bắt đầu hiển thị
            self.alert_duration = alert_duration

    def update_alert(self):
        """
        Cập nhật thông báo và hiển thị nếu show_alert là True. Kiểm tra thời gian hiển thị của thông báo.
        """
        if self.show_alert:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.alert_start_time

            # Điều chỉnh vị trí và độ trong suốt dựa trên thời gian hiện tại
            # Hiệu ứng rơi từ trên xuống
            if elapsed_time < self.alert_duration:
                # Tính toán vị trí hiện tại (rơi từ trên xuống)
                drop_duration = 500  # Thời gian cho hiệu ứng rơi (500ms)
                target_y = 20  # Vị trí y cố định khi alert dừng lại

                if elapsed_time < drop_duration:
                    # Dùng easing để rơi từ từ (công thức easing linear đơn giản)
                    y_pos = int(-50 + (target_y + 50) * (elapsed_time / drop_duration))
                else:
                    y_pos = target_y

                # Hiệu ứng rõ dần khi xuất hiện (fade-in)
                fade_in_duration = 500  # Thời gian cho hiệu ứng rõ dần (300ms)
                if elapsed_time < fade_in_duration:
                    alpha = int(255 * (elapsed_time / fade_in_duration))  # Độ trong suốt tăng dần
                else:
                    alpha = 255

            # Khi đã gần hết thời gian alert
            elif elapsed_time >= self.alert_duration:
                fade_out_duration = 350  # Thời gian cho hiệu ứng mờ dần và di chuyển lên (500ms)
                time_since_fade = elapsed_time - self.alert_duration

                if time_since_fade < fade_out_duration:
                    # Mờ dần và di chuyển lên
                    y_pos = 20 - int(30 * (time_since_fade / fade_out_duration))
                    alpha = int(255 * (1 - time_since_fade / fade_out_duration))
                else:
                    # Kết thúc hiệu ứng, tắt alert
                    self.show_alert = False
                    return

            # Chia text thành nhiều dòng nếu quá dài
            wrapped_lines = self.wrap_text(self.alert_text, self.get_font(15), 350)

            # Tính chiều cao và rộng của background dựa trên số dòng text
            alert_bg_height = len(wrapped_lines) * self.get_font(15).get_height() + 20
            alert_bg_width = max(self.get_font(15).size(line)[0] for line in wrapped_lines) + 30

            # Tính vị trí của alert
            alert_bg_rect = pygame.Rect(1240 - alert_bg_width - 20, y_pos, alert_bg_width, alert_bg_height)

            # Màu sắc với độ trong suốt (alpha)
            bg_color = (255, 255, 255, alpha)  # Nền trắng với độ trong suốt
            border_color = (0, 0, 0)  # Viền đen

            # Hiệu ứng đổ bóng (shadow)
            shadow_offset = 5
            shadow_rect = alert_bg_rect.move(shadow_offset, shadow_offset)
            shadow_color = (50, 50, 50, alpha // 2)  # Đổ bóng với độ trong suốt nhẹ

            # Vẽ đổ bóng
            pygame.draw.rect(self.display_surface, shadow_color, shadow_rect, border_radius=20)

            # Vẽ nền thông báo
            pygame.draw.rect(self.display_surface, bg_color, alert_bg_rect, border_radius=20)

            # Vẽ viền xung quanh nền thông báo
            pygame.draw.rect(self.display_surface, border_color, alert_bg_rect, 3, border_radius=20)

            # Hiển thị từng dòng text
            for i, line in enumerate(wrapped_lines):
                alert_text_surface = self.get_font(15).render(line, True, "Black")
                alert_text_surface.set_alpha(alpha)  # Cài đặt độ trong suốt cho text
                line_height = self.get_font(15).get_height()
                line_y_pos = alert_bg_rect.top + (i * line_height) + 10
                alert_text_rect = alert_text_surface.get_rect(center=(alert_bg_rect.centerx, line_y_pos + line_height // 2))
                self.display_surface.blit(alert_text_surface, alert_text_rect)


        else:
            # Tắt alert sau khi hết thời gian hiển thị
            self.show_alert = False