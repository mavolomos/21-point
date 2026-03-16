import tkinter as tk
from tkinter import messagebox
import random

rank = [2, 3, 4, 5, 6, 7, 8, 9, 'T', 'J', 'Q', 'K', 'A']
suit = ['♠', '♥', '♦', '♣']

def make_desk():
    desk = []
    for r in rank:
        for s in suit:
            card = str(r) + str(s)
            desk.append(card)
    return desk

def make_color(hand):
    new_hand = []
    for card in hand:
        card = card.replace('T', '10')
        new_hand.append(card)
    return new_hand

def count_score(hand):
    score = 0
    for card in hand:
        if card[0] in ['J', 'Q', 'K', 'T'] or card[:2] == '10':
            score += 10
        elif card[0] == 'A':
            score += 11
        else:
            score += int(card[0])
    return score

# ========== GUI на tkinter ==========
class BlackjackGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("21 очко")
        self.root.geometry("400x300")
        self.game_window = None  # ссылка на текущее окно игры
        self.main_menu()
        self.root.mainloop()

    def main_menu(self):
        """Главное меню с кнопками."""
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Добро пожаловать в игру 21 очко!",
                 font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Новая игра", command=self.new_game,
                  width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Правила", command=self.show_rules,
                  width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Выход", command=self.root.quit,
                  width=20, height=2).pack(pady=10)

    def show_rules(self):
        """Окно с правилами (второе окно)."""
        rules_window = tk.Toplevel(self.root)
        rules_window.title("Правила")
        rules_window.geometry("300x200")
        rules_text = """Цель игры - набрать 21 очко или близко к нему, но не больше.
Карты от 2 до 9 - по номиналу.
T, J, Q, K - 10 очков.
Туз - 11 очков.
Крупье сдает по 2 карты себе и игроку.
Игрок может взять еще карту или остановиться.
Если у игрока больше 21 - он проигрывает.
Если у крупье больше 21 - выигрывает игрок.
Иначе сравниваются суммы очков."""
        tk.Label(rules_window, text=rules_text, justify=tk.LEFT,
                 padx=10, pady=10).pack()
        tk.Button(rules_window, text="Закрыть",
                  command=rules_window.destroy).pack(pady=10)

    def close_game_window(self):
        """Закрывает игровое окно и обнуляет ссылку."""
        if self.game_window and self.game_window.winfo_exists():
            self.game_window.destroy()
        self.game_window = None

    def new_game(self):
        """Создание окна игры, предварительно закрывая предыдущее."""
        self.close_game_window()  # закрываем старое окно, если оно есть

        self.game_window = tk.Toplevel(self.root)
        self.game_window.title("Игра")
        self.game_window.geometry("500x400")
        self.game_window.protocol("WM_DELETE_WINDOW", self.close_game_window)

        # Инициализация колоды и рук
        self.deck = make_desk()
        self.deck = random.sample(self.deck, len(self.deck))
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False

        # Начальная раздача (по 2 карты)
        self.dealer_hand.append(self.deck.pop())
        self.player_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())
        self.player_hand.append(self.deck.pop())

        # Поле для ввода (имя игрока)
        tk.Label(self.game_window, text="Ваше имя:").grid(
            row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.game_window)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_entry.insert(0, "Игрок")

        # Метки для карт
        tk.Label(self.game_window, text="Карты крупье:",
                 font=("Arial", 12)).grid(row=1, column=0, columnspan=2, pady=5)
        self.dealer_label = tk.Label(self.game_window, text="",
                                      font=("Arial", 14))
        self.dealer_label.grid(row=2, column=0, columnspan=2, pady=5)

        tk.Label(self.game_window, text="Ваши карты:",
                 font=("Arial", 12)).grid(row=3, column=0, columnspan=2, pady=5)
        self.player_label = tk.Label(self.game_window, text="",
                                      font=("Arial", 14))
        self.player_label.grid(row=4, column=0, columnspan=2, pady=5)

        self.score_label = tk.Label(self.game_window, text="Счет: 0",
                                     font=("Arial", 12))
        self.score_label.grid(row=5, column=0, columnspan=2, pady=5)

        # Кнопки действий
        self.hit_button = tk.Button(self.game_window, text="Взять карту",
                                     command=self.hit, width=15, height=2)
        self.hit_button.grid(row=6, column=0, padx=10, pady=10)
        self.stand_button = tk.Button(self.game_window, text="Остановиться",
                                       command=self.stand, width=15, height=2)
        self.stand_button.grid(row=6, column=1, padx=10, pady=10)

        self.new_game_button = tk.Button(self.game_window, text="Новая игра",
                                          command=self.restart_game,
                                          width=15, height=2)
        self.new_game_button.grid(row=7, column=0, columnspan=2, pady=10)
        self.new_game_button.config(state=tk.DISABLED)

        self.update_display()

    def restart_game(self): #перезапуск игры
        self.game_window.destroy()
        self.new_game()

    def update_display(self): #обновление карт
        if not self.game_over:
            # Крупье: первая карта открыта, остальные скрыты
            dealer_cards = [make_color([self.dealer_hand[0]])[0]] + \
                           ["[XX]"] * (len(self.dealer_hand) - 1)
        else:
            # Все карты открыты
            dealer_cards = make_color(self.dealer_hand)

        self.dealer_label.config(text=" | ".join(dealer_cards))
        self.player_label.config(text=" | ".join(make_color(self.player_hand)))
        self.score_label.config(text=f"Счет: {count_score(self.player_hand)}")

    def hit(self):
        if self.game_over:
            return
        if not self.deck:
            messagebox.showwarning("Колода пуста", "Карты закончились!")
            self.end_game()
            return

        self.player_hand.append(self.deck.pop())
        self.update_display()

        # Проверка перебора у игрока
        if count_score(self.player_hand) >= 21:
            self.end_game()
            return

        # Ход крупье (одна карта, если его счёт <= 10)
        if count_score(self.dealer_hand) <= 10 and self.deck:
            self.dealer_hand.append(self.deck.pop())
            self.update_display()
            if count_score(self.dealer_hand) >= 21:
                self.end_game()

    def stand(self):
        if self.game_over:
            return

        # Крупье берёт одну карту, если его счёт <= 10
        if count_score(self.dealer_hand) <= 10 and self.deck:
            self.dealer_hand.append(self.deck.pop())
            self.update_display()

        self.end_game()

    def end_game(self):
        """Завершение игры: подсчёт результатов и показ."""
        self.game_over = True
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.new_game_button.config(state=tk.NORMAL)

        # Показываем все карты крупье
        self.update_display()

        player_score = count_score(self.player_hand)
        dealer_score = count_score(self.dealer_hand)

        # Определение результата
        if player_score > 21:
            result = "Вы проиграли :("
        elif dealer_score > 21:
            result = "Вы выиграли! :)"
        elif player_score > dealer_score:
            result = "Вы выиграли! :)"
        elif player_score < dealer_score:
            result = "Вы проиграли :("
        else:
            result = "Ничья"

        messagebox.showinfo("Результат", result)

# ========== Запуск GUI ==========
if __name__ == "__main__":
    app = BlackjackGUI()