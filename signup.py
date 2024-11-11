import customtkinter as ctk
import requests
import re

class SignupFrame:
    def __init__(self, parent, show_frame_callback):
        self.frame = parent
        self.show_frame_callback = show_frame_callback
        self.title_font = ctk.CTkFont(family="NanumBarunpenR", size=24, weight="bold")
        self.description_font = ctk.CTkFont(family="NanumBarunpenR", size=16, weight="bold")
        self.create_widgets()

    def create_widgets(self):
        # 제목 라벨 생성
        title_label = ctk.CTkLabel(self.frame, text="회원가입", font=self.title_font)
        title_label.pack(pady=20, padx=60)

        # 설명 라벨 생성
        description_label = ctk.CTkLabel(self.frame, text="정보를 입력하세요", font=self.description_font)
        description_label.pack(pady=10, padx=60)

        # 학번/교직원 번호 입력 필드 생성
        self.entry_number = ctk.CTkEntry(self.frame, placeholder_text="학번 또는 교직원 번호", font=self.description_font, width=200)
        self.entry_number.pack(pady=10, padx=60)

        # 사용자 이름 입력 필드 생성
        self.entry_username = ctk.CTkEntry(self.frame, placeholder_text="사용자 이름", font=self.description_font, width=200)
        self.entry_username.pack(pady=10, padx=60)

        # 비밀번호 입력 필드 생성
        self.entry_password = ctk.CTkEntry(self.frame, placeholder_text="비밀번호", show="*", font=self.description_font, width=200)
        self.entry_password.pack(pady=10, padx=10)

        # 비밀번호 확인 입력 필드 생성
        self.entry_confirm_password = ctk.CTkEntry(self.frame, placeholder_text="비밀번호 확인", show="*", font=self.description_font, width=200)
        self.entry_confirm_password.pack(pady=10, padx=10)

        # 이메일 입력 필드 생성
        self.entry_email = ctk.CTkEntry(self.frame, placeholder_text="이메일 주소", font=self.description_font, width=200)
        self.entry_email.pack(pady=10, padx=10)

        # 이메일 입력 후 엔터키를 눌렀을 때 회원가입 함수 호출
        self.entry_email.bind('<Return>', self.signup)

        # 회원가입 버튼 생성
        signup_button = ctk.CTkButton(self.frame, text="회원가입", command=self.signup, font=self.description_font)
        signup_button.pack(pady=20, padx=60)

        # 로그인 페이지로 돌아가는 링크 버튼 생성
        login_link = ctk.CTkButton(self.frame, text="로그인 페이지로 돌아가기", fg_color="transparent", text_color="#0487f9", hover_color="#E0E0E0", command=lambda: self.show_frame_callback('login'), font=self.description_font)
        login_link.pack(pady=10, padx=60)

    def signup(self, event=None):
        # 입력 필드가 비어 있는지 확인
        if not self.entry_number.get() or not self.entry_username.get() or not self.entry_password.get() or not self.entry_confirm_password.get() or not self.entry_email.get():
            self.show_alert("모든 필드를 채우세요.")
            return

        # 이메일 유효성 검사
        email = self.entry_email.get()
        email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
        if not re.match(email_pattern, email):
            self.show_alert("유효한 이메일 주소를 입력하세요.")
            return

        # 비밀번호 일치 여부 확인
        if self.entry_password.get() != self.entry_confirm_password.get():
            self.show_alert("비밀번호가 일치하지 않습니다.")
            return

        # 학번/교직원 번호 유효성 검사 (예시: 숫자만 허용)
        if not self.entry_number.get().isdigit():
            self.show_alert("학번 또는 교직원 번호는 숫자여야 합니다.")
            return

        # 데이터 딕셔너리 생성
        data = {
            'student_staff_number': self.entry_number.get(),
            'username': self.entry_username.get(),
            'password': self.entry_password.get(),
            'confirm_password': self.entry_confirm_password.get(),
            'email': self.entry_email.get()
        }

        try:
            # 서버에 회원가입 요청
            response = requests.post('http://61.255.152.191:5000/signup', json=data)
            response_data = response.json()

            if response.status_code == 200 and response_data.get("status") == "success":
                self.show_alert("회원가입 성공!")
                self.show_frame_callback('login')
            else:
                error_detail = response_data.get("detail", "알 수 없는 오류가 발생했습니다.")
                self.show_alert(error_detail)

        except requests.RequestException as e:
            self.show_alert(f"요청 중 오류가 발생했습니다: {e}")

    def show_alert(self, message):
        # 경고창 생성
        alert = ctk.CTkToplevel(self.frame)
        alert.title("경고")
        alert.geometry("300x150")

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
