import customtkinter as ctk
import requests
import re

class PasswordResetFrame:
    def __init__(self, frame, show_frame_callback):
        self.frame = frame
        self.show_frame_callback = show_frame_callback
        self.create_widgets()
    
    def create_widgets(self):
        title_font = ctk.CTkFont(family="NanumBarunpenR", size=24, weight="bold")
        self.description_font = ctk.CTkFont(family="NanumBarunpenR", size=16, weight="bold")

        # 제목 라벨 생성
        title_label = ctk.CTkLabel(self.frame, text="비밀번호 찾기", font=title_font)
        title_label.pack(pady=20, padx=60)

        # 설명 라벨 생성
        description_label = ctk.CTkLabel(self.frame, text="이메일 주소를 입력하세요", font=self.description_font)
        description_label.pack(pady=10, padx=60)

        # 이메일 입력 필드 생성
        self.entry_email = ctk.CTkEntry(self.frame, placeholder_text="이메일 주소", font=self.description_font, width=200)
        self.entry_email.pack(pady=10, padx=60)

        # 비밀번호 재설정 버튼 생성
        reset_button = ctk.CTkButton(self.frame, text="비밀번호 받기", command=self.reset_password, font=self.description_font)
        reset_button.pack(pady=20, padx=60)

        # 로그인 페이지로 돌아가기 링크 생성
        back_to_login_link = ctk.CTkButton(self.frame, text="로그인 페이지로 돌아가기", fg_color="transparent", text_color="#0487f9", hover_color="#E0E0E0", command=lambda: self.show_frame_callback('login'), font=self.description_font)
        back_to_login_link.pack(pady=10, padx=60)

        # 엔터키를 눌렀을 때 비밀번호 재설정 함수 호출
        self.entry_email.bind('<Return>', self.reset_password)

    def show_alert(self, message):
        # 경고창 생성
        alert = ctk.CTkToplevel(self.frame)
        alert.title("경고")
        alert.geometry("350x150")

        alert_label = ctk.CTkLabel(alert, text=message, font=self.description_font)
        alert_label.pack(pady=20)

        close_button = ctk.CTkButton(alert, text="닫기", command=alert.destroy)
        close_button.pack(pady=20)

        alert.transient(self.frame)
        alert.grab_set()
        alert.lift()
        alert.attributes('-topmost', True)
        alert.resizable(False, False)

        alert.update_idletasks()
        parent_window = self.frame.winfo_toplevel()
        window_width = alert.winfo_width()
        window_height = alert.winfo_height()
        screen_width = parent_window.winfo_screenwidth()
        screen_height = parent_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        alert.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def reset_password(self, event=None):
        # 이메일 입력값 가져오기
        email = self.entry_email.get()
        if not email:
            self.show_alert("이메일 주소를 입력하세요.")
            return
        
        # 이메일 형식 유효성 검사
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            self.show_alert("유효한 이메일 주소를 입력하세요.")
            return

        data = {'email': email}
        try:
            # 서버에 비밀번호 재설정 요청
            response = requests.post('http://61.255.152.191:5000/password_reset', json=data)
            response_data = response.json()
            print(response_data)  # 응답 데이터 출력하여 디버깅
            if response.status_code == 200:
                self.show_alert("비밀번호 재설정 링크가 이메일로 전송되었습니다.")
            else:
                error_detail = response.json().get("detail", "알 수 없는 오류가 발생했습니다.")
                if isinstance(error_detail, list):
                    error_messages = "\n".join([error.get('msg', '알 수 없는 오류가 발생했습니다.') for error in error_detail])
                    self.show_alert(error_messages)
                else:
                    self.show_alert(error_detail)
        except requests.RequestException as e:
            self.show_alert(f"요청 중 오류가 발생했습니다: {e}")

# 예시: 이 코드를 호출하여 프레임을 생성합니다.
# frame = ctk.CTkFrame(root)
# PasswordResetFrame(frame, show_frame)
# frame.pack(fill="both", expand=True)
