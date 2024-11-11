import customtkinter as ctk
from PIL import Image
import os
from signup import SignupFrame
from login import LoginFrame
from password_reset import PasswordResetFrame
from inbox import Inbox

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("전주대학교 메일")
        
        # 배경 이미지 설정
        self.setup_background()
        
        # 각 프레임의 페이지 크기 정의
        self.page_sizes = {
            'login': (401, 500),
            'signup': (401, 645),
            'password_reset': (401, 450),  # 비밀번호 재설정 프레임 크기
        }
        
        # 둥근 모서리와 검은 배경을 가진 외부 프레임 생성
        self.outer_frame = ctk.CTkFrame(root, corner_radius=13, fg_color="black")
        self.outer_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # 프레임 딕셔너리 초기화
        self.frames = {}
        
        # 각 페이지에 대한 개별 프레임 생성
        self.create_frames()
        
        # 초기 페이지 (로그인 페이지) 표시
        self.show_frame('login')
    
    def setup_background(self):
        # 배경 이미지 경로 정의
        background_image_path = os.path.join(os.path.dirname(__file__), "background.jpg")
        
        # PIL을 사용하여 이미지 로드 및 크기 조정
        background_image = Image.open(background_image_path)
        background_image_resized = background_image.resize((1218, 685), Image.LANCZOS)
        
        # 이미지를 CTkImage로 변환
        background_photo = ctk.CTkImage(light_image=background_image_resized, size=(1218, 685))
        
        # 배경 이미지를 표시할 라벨 생성
        background_label = ctk.CTkLabel(self.root, image=background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # 창 크기를 배경 이미지에 맞게 조정
        window_width, window_height = background_image_resized.size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)  # 창 크기 고정
    
    def create_frames(self):
        # 각 페이지에 대한 프레임 생성 및 프레임 딕셔너리에 저장
        for frame_name in ('login', 'signup', 'password_reset'):
            frame = ctk.CTkFrame(self.outer_frame, corner_radius=10, fg_color="white")
            self.frames[frame_name] = frame
        
        # 각 프레임을 해당 내용으로 초기화
        LoginFrame(self.frames['login'], self.show_frame)
        SignupFrame(self.frames['signup'], self.show_frame)
        PasswordResetFrame(self.frames['password_reset'], self.show_frame)
    
    def show_frame(self, frame_name, *args):
        # 모든 프레임 숨기기
        for frame in self.frames.values():
            frame.pack_forget()
        
        if frame_name == 'inbox':
            # 인박스 페이지가 요청되면 현재 창을 닫고 새 창 열기
            self.root.destroy()  # 로그인 창 닫기
            new_root = ctk.CTk()
            new_root.geometry("800x600")
            inbox_instance = Inbox(new_root, *args)
            new_root.mainloop()
        else:
            # 요청된 프레임의 크기 가져오기
            width, height = self.page_sizes[frame_name]
            self.outer_frame.configure(width=width - 75, height=height - 162)
            
            # 모든 프레임 숨기고 요청된 프레임 표시
            for frame in self.frames.values():
                frame.place_forget()
            self.frames[frame_name].place(relx=0.5, rely=0.5, anchor='center')

    def run(self):
        # Tkinter 메인 루프 시작
        self.root.mainloop()

if __name__ == '__main__':
    root = ctk.CTk()
    app = App(root)
    app.run()
