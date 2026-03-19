import flet as ft
import time
import speech_recognition as sr
import threading

# --- ГЛОБАЛНИ НАСТРОЙКИ И МЕСТОИМЕНИЯ ---
class GlobalAI:
    def __init__(self):
        self.current_lang = "BG"
        # Речник с местоимения за целия свят
        self.data = {
            "BG": {"i": "Аз", "we": "Ние", "you": "Ти", "he": "Той", "she": "Тя", "it": "То", "they": "Те", "vote": "гласувам", "success": "Гласува успешно!"},
            "EN": {"i": "I", "we": "We", "you": "You", "he": "He", "she": "She", "it": "It", "they": "They", "vote": "vote", "success": "Voted successfully!"},
            "ES": {"i": "Yo", "we": "Nosotros", "you": "Tú", "he": "Él", "she": "Ella", "it": "Eso", "they": "Ellos", "vote": "voto", "success": "¡Votado con éxito!"},
            "DE": {"i": "Ich", "we": "Wir", "you": "Du", "he": "Er", "she": "Sie", "it": "Es", "they": "Sie", "vote": "stimme", "success": "Erfolgreich gewählt!"}
        }

def main(page: ft.Page):
    ai = GlobalAI()
    page.title = "Universal SmartVote AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700
    page.padding = 30

    # Променливи за състоянието
    status_text = ft.Text("ДОКОСНИ ИЛИ ГОВОРИ", size=25, weight="bold", text_align="center")
    info_label = ft.Text("Ние променяме света", italic=True, color="blue200")
    
    # Сърцето на системата: Тактилен Морзов сигнал за сляпо-глухи (П-О-Т-В-Ъ-Р-Д-Е-Н-О)
    def trigger_vibration():
        # Симулация на вибрационен сигнал през екрана за тези, които не чуват и не виждат
        pulses = [0.1, 0.1, 0.4, 0.1, 0.4, 0.4] # Кратко-дълго-дълго
        for p in pulses:
            page.bgcolor = "white" # Визуален импулс
            page.update()
            time.sleep(p)
            page.bgcolor = ft.colors.SURFACE_VARIANT
            page.update()
            time.sleep(0.1)

    # Гласов анализ (за слепи и хора без крайници)
    def start_listening(e):
        def recognize():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                status_text.value = "СЛУШАМ..."
                page.update()
                try:
                    audio = r.listen(source, timeout=4)
                    text = r.recognize_google(audio, language=ai.current_lang.lower()).lower()
                    # ИИ търси ключово местоимение "Аз" или "I" или "Yo"
                    if any(word in text for word in [ai.data[ai.current_lang]["i"].lower(), ai.data[ai.current_lang]["vote"]]):
                        process_universal_vote()
                    else:
                        status_text.value = "НЕ ВИ РАЗБРАХ"
                        page.update()
                except:
                    status_text.value = "ГРЕШКА В ГЛАСА"
                    page.update()
        
        threading.Thread(target=recognize).start()

    # Универсално приемане на вота
    def process_universal_vote(e=None):
        t = ai.data[ai.current_lang]
        # Обединяваме местоименията: "Ти (you) гласува успешно"
        status_text.value = f"{t['you']} {t['success']}"
        status_text.color = "green"
        page.update()
        # Изпращаме тактилния сигнал към кожата
        trigger_vibration()

    # Смяна на езика (Световен мащаб)
    def set_language(lang_code):
        ai.current_lang = lang_code
        status_text.value = "READY / ГОТОВ"
        page.update()

    # ГРАФИЧЕН ИНТЕРФЕЙС (Единна повърхност)
    page.add(
        ft.Row([
            ft.TextButton("BG", on_click=lambda _: set_language("BG")),
            ft.TextButton("EN", on_click=lambda _: set_language("EN")),
            ft.TextButton("ES", on_click=lambda _: set_language("ES")),
            ft.TextButton("DE", on_click=lambda _: set_language("DE")),
        ], alignment="center"),
        ft.Divider(height=40, color="transparent"),
        ft.GestureDetector(
            on_tap=process_universal_vote, # За всички (допир)
            on_long_press=start_listening, # За слепи (глас)
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.FINGERPRINT, size=80, color="blue"),
                    status_text,
                    info_label,
                    ft.Text("\n(Докосни за вот)\n(Задръж за глас)", size=12, text_align="center")
                ], horizontal_alignment="center"),
                padding=40,
                border=ft.border.all(3, "blue"),
                border_radius=30,
                bgcolor=ft.colors.SURFACE_VARIANT
            )
        )
    )

ft.app(target=main)
