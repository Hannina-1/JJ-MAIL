import customtkinter as ctk
import requests

class LoginFrame:
    def __init__(self, parent, login_success_callback):
        self.parent = parent
        self.login_success_callback = login_success_callback
        self.title_font = ctk.CTkFont(family="NanumBarunpenR", size=24, weight="bold")
        self.description_font = ctk.CTkFont(family="NanumBarunpenR", size=16, weight="bold")
        self.create_widgets()

    def create_widgets(self):
        # 제목 라벨 생성
        title_label = ctk.CTkLabel(self.parent, text="전주대학교 메일", font=self.title_font)
        title_label.pack(pady=20, padx=10)

        # 설명 라벨 생성
        description_label = ctk.CTkLabel(self.parent, text="로그인하세요", font=self.description_font)
        description_label.pack(pady=10, padx=10)

        # 학번/교직원 번호 입력 필드 생성
        self.entry_number = ctk.CTkEntry(self.parent, placeholder_text="학번 또는 교직원 번호", font=self.description_font, width=200)
        self.entry_number.pack(pady=10, padx=10)

        # 비밀번호 입력 필드 생성
        self.entry_password = ctk.CTkEntry(self.parent, placeholder_text="비밀번호", show="*", font=self.description_font, width=200)
        self.entry_password.pack(pady=10, padx=10)

        # 비밀번호 입력 후 엔터 키를 누르면 로그인
        self.entry_password.bind('<Return>', self.login)

        # 로그인 버튼 생성
        login_button = ctk.CTkButton(self.parent, text="로그인", command=self.login, font=self.description_font)
        login_button.pack(pady=20, padx=10)

        # 링크들을 담을 프레임 생성
        links_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        links_frame.pack(pady=10, padx=10)

        # 회원가입 링크 버튼 생성
        signup_link = ctk.CTkButton(links_frame, text="회원가입", fg_color="transparent", text_color="#0487f9", hover_color="#E0E0E0", command=lambda: self.login_success_callback('signup'), font=self.description_font)
        signup_link.pack(side="left", padx=5)

        # 비밀번호 찾기 링크 버튼 생성
        password_reset_link = ctk.CTkButton(links_frame, text="비밀번호 찾기", fg_color="transparent", text_color="#0487f9", hover_color="#E0E0E0", command=lambda: self.login_success_callback('password_reset'), font=self.description_font)
        password_reset_link.pack(side="left", padx=5)

    def login(self, event=None):
        # 로그인 요청 데이터 생성
        data = {
            'student_staff_number': self.entry_number.get(),
            'password': self.entry_password.get()
        }
        # 서버로 로그인 요청 전송
        response = requests.post('http://61.255.152.191:5000/login', json=data)
        # 로그인 성공 시
        if response.json().get("status") == "success":
            username = data['student_staff_number']
            user_fullname = response.json().get("username")
            self.login_success_callback('inbox', username, user_fullname)
        else:
            # 로그인 실패 시 경고 메시지 표시
            self.show_alert("로그인 실패!")

    def show_alert(self, message):
        # 경고 창 생성
        alert = ctk.CTkToplevel(self.parent)
        alert.title("경고")
        alert.geometry("300x150")

        # 경고 메시지 라벨 생성
        alert_label = ctk.CTkLabel(alert, text=message, font=self.description_font)
        alert_label.pack(pady=20)

        # 닫기 버튼 생성
        close_button = ctk.CTkButton(alert, text="닫기", command=alert.destroy)
        close_button.pack(pady=20)

        # 경고 창을 부모 창 위로 표시
        alert.transient(self.parent)
        alert.grab_set()
        alert.lift()
        alert.attributes('-topmost', True)
        alert.resizable(False, False)

        # 경고 창을 화면 중앙에 위치시키기 위한 계산
        alert.update_idletasks()
        parent_window = self.parent.winfo_toplevel()
        window_width = alert.winfo_width()
        window_height = alert.winfo_height()
        screen_width = parent_window.winfo_screenwidth()
        screen_height = parent_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        alert.geometry(f"{window_width}x{window_height}+{x}+{y}")

if __name__ == '__main__':
    root = ctk.CTk()
    root.geometry("400x500")

    frame = ctk.CTkFrame(root)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # 로그인 프레임 생성
    LoginFrame(frame, lambda frame_name: print(f"Switch to {frame_name} frame"))

    root.mainloop()
