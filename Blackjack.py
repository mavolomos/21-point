import tkinter as tk
from tkinter import messagebox
import random
import json 
import os
from datetime import datetime

#колода
rank = [2, 3, 4, 5, 6, 7, 8, 9, 'T', 'J', 'Q', 'K', 'A']
suit = ['♠', '♥', '♦', '♣']

#создание колоды и возращение ее
def create_deck():
    deck = []
    for r in rank:
        for s in suit:
            deck.append(str(r) + s)
    return deck

#замена формта карты 10
def format_card(card):
    if card[0] == 'T':
        return '10' + card[1]
    return card

#возращение строчки с новым форматом карт
def format_hand(hand):
    return ' | '.join(format_card(c) for c in hand) #ставим палку между картами для красоты

#счет функция
def count_score(hand):
    score = 0
    for card in hand:
        r = card[0]
        if r in ('J', 'Q', 'K', 'T'):
            score += 10
        elif r == 'A':
            score += 11
        else:
            score += int(r)
    return score

# отдельный класс для функций самого процесса игры
class Game:
    def __init__(self): #
        self.deck = [] #список пустой колоды
        self.player_hand = [] #список карт игрока
        self.dealer_hand = [] #список карт крупье
        self.game_over = False #флаг, когда кто-то набирае ольше 21 очка или игра завершена, блокирует действия дальше
        self.player_name = "Игрок" #Имя игрока
        self.new_deck() #перемешанная колода

#создание и перемешка колоды
    def new_deck(self):
        self.deck = create_deck()
        random.shuffle(self.deck)

#функция для раздачи карт игроку и крупье, и сразу удаляет эти карты из колоды
    def deal_initial(self):
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.game_over = False #сброс флага


    def player_hit(self):
        if not self.game_over: #если игра не закончилась игрок берет карту
            self.player_hand.append(self.deck.pop())
            if count_score(self.player_hand) > 21: #подсчет очков
                self.game_over = True

#то же самое что и player_hit только для крупье
    def dealer_hit(self):
        if not self.game_over:
            self.dealer_hand.append(self.deck.pop())
            if count_score(self.dealer_hand) > 21:
                self.game_over = True

#функция для ттго что бы крупье брал карты токлько когда у негоо меньше 10 очков
    def dealer_play(self):
        while not self.game_over and count_score(self.dealer_hand) <= 10:
            self.dealer_hit()

#функия определения победителя 
    def get_winner(self):
        player_score = count_score(self.player_hand)
        dealer_score = count_score(self.dealer_hand)
        if player_score > 21:
            return "дилер"
        if dealer_score > 21:
            return "игрок"
        if player_score > dealer_score:
            return "игрок"
        if dealer_score > player_score:
            return "дилер"
        return "ничья"

# создание стартового окна
class StartWindow:
    def __init__(self, master):
        self.master = master
        master.title("21 очко - Добро пожаловать")
        master.geometry("300x200")
        master.resizable(False, False)

        tk.Label(master, text="Добро пожаловать в игру 21 очко!",
                 font=("Arial", 12)).pack(pady=20)

        tk.Label(master, text="Введите ваше имя:").pack() # поле с вводом имени
        self.name_entry = tk.Entry(master, width=25)
        self.name_entry.pack(pady=5)
        self.name_entry.focus() # установка курсора в окне

        tk.Button(master, text="Начать игру", command=self.start_game,
                  bg="lightblue").pack(pady=20)

    def start_game(self):
        player_name = self.name_entry.get().strip() #вносит в коно данные об имени игрока и strip удаляет пробелы по краям 
        if not player_name:
            player_name = "Игрок"  # если имени нет, то оставляем игрок
        self.master.destroy() # закрывает стартовое окно
        root = tk.Tk() # создаём главное окно игры
        GameWindow(root, player_name)
        root.mainloop() #передача управления

#игровое окно
class GameWindow:
    def __init__(self, master, player_name):
        self.master = master
        master.title("21 очко - Игра")
        master.geometry("600x500")
        master.resizable(False, False)

        self.game = Game()
        self.game.player_name = player_name

        # верхняя панель с именем
        tk.Label(master, text=f"Игрок: {player_name}",
                 font=("Arial", 14)).pack(pady=5)

        # панель крупье
        self.dealer_frame = tk.LabelFrame(master, text="Крупье",
                                          font=("Arial", 12), padx=10, pady=10) #имя крупье
        self.dealer_frame.pack(pady=10, fill="x", padx=20)

        self.dealer_cards_label = tk.Label(self.dealer_frame,
                                           text="", font=("Courier", 14)) # карты крупье, показывается 1
        self.dealer_cards_label.pack()

        self.dealer_score_label = tk.Label(self.dealer_frame,
                                           text="Счёт: ?", font=("Arial", 10)) #счет крупье
        self.dealer_score_label.pack()

        # панель игрока
        self.player_frame = tk.LabelFrame(master, text="Ваши карты",
                                          font=("Arial", 12), padx=10, pady=10)
        self.player_frame.pack(pady=10, fill="x", padx=20)

        self.player_cards_label = tk.Label(self.player_frame,
                                           text="", font=("Courier", 14)) #карты игрока
        self.player_cards_label.pack()

        self.player_score_label = tk.Label(self.player_frame,
                                           text="Счёт: 0", font=("Arial", 10)) #счет игрока
        self.player_score_label.pack()

        # панель кнопок для игрока
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=20)

        self.hit_button = tk.Button(self.button_frame, text="Взять карту (Hit)",
                                    command=self.hit, bg="lightgreen", width=15)
        self.hit_button.grid(row=0, column=0, padx=5)

        self.stand_button = tk.Button(self.button_frame, text="Хватит (Stand)",
                                      command=self.stand, bg="lightcoral", width=15)
        self.stand_button.grid(row=0, column=1, padx=5)

        self.new_game_button = tk.Button(self.button_frame, text="Новая игра",
                                         command=self.new_game, bg="lightyellow", width=15)
        self.new_game_button.grid(row=0, column=2, padx=5)

        self.rules_button = tk.Button(self.button_frame, text="Правила",
                                      command=self.show_rules, bg="lightgray", width=15)
        self.rules_button.grid(row=0, column=3, padx=5)

        self.quit_button = tk.Button(self.button_frame, text="Выход",
                                     command=master.quit, bg="lightgray", width=15)
        self.quit_button.grid(row=0, column=4, padx=5)

        # начало первого раунда
        self.new_round()
#сброс игрового состояния для нового раунда
    def new_round(self):
        self.game.new_deck() #перемешка колоды
        self.game.deal_initial() #начальные карты
        self.update_display(show_dealer_full=False) #обновление изображения, одна карта у крупье
        #разблокировка кнопок
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)

#обновление текста в окне
    def update_display(self, show_dealer_full=False):
        if show_dealer_full: #показ карт крпуье и счета
            dealer_cards = [format_card(c) for c in self.game.dealer_hand]
            dealer_score = count_score(self.game.dealer_hand)
        else: #ничегт не показывает у крупье
            dealer_cards = [format_card(self.game.dealer_hand[0]), "XX"]
            dealer_score = "?"

        #форматирование для дилера
        self.dealer_cards_label.config(text=" | ".join(dealer_cards))
        self.dealer_score_label.config(text=f"Счёт: {dealer_score}")

        #форматирование для игрока 
        player_cards = [format_card(c) for c in self.game.player_hand]
        self.player_cards_label.config(text=" | ".join(player_cards))
        player_score = count_score(self.game.player_hand)
        self.player_score_label.config(text=f"Счёт: {player_score}")

    #обработчик нажатия "взять карту"
    def hit(self):
        self.game.player_hit() #добавляет карту и проверяет перебор по очкам
        self.update_display(show_dealer_full=False) #обновление отображения

        if self.game.game_over: 
            self.end_game() #конец игры
            return

        # ход крупье, если у него ≤10
        if count_score(self.game.dealer_hand) <= 10:
            self.game.dealer_hit() #крупье берет карту
            self.update_display(show_dealer_full=False) #обновление отображения у крупье
            if self.game.game_over:
                self.end_game()

    #обработчик нажатия "хватит"
    def stand(self):
        self.game.dealer_play() #добор карт крупье
        self.update_display(show_dealer_full=True) #показ карт крупье
        self.end_game()

    #конец игры
    def end_game(self):
        self.update_display(show_dealer_full=True)
        winner = self.game.get_winner() #определения победителя
        if winner == "игрок":
            msg = f"{self.game.player_name} выиграл! Поздравляем!"
        elif winner == "дилер":
            msg = "Крупье выиграл. Повезёт в следующий раз."
        else:
            msg = "Ничья."

        messagebox.showinfo("Игра окончена", msg) #вывод результата
        #блокировка кнопок
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)

    #новый раунд(не первый)
    def new_game(self):
        self.game.new_deck()
        self.game.deal_initial()
        self.update_display(show_dealer_full=False)
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)

    #доп окно с правилами игры
    def show_rules(self):
        rules_win = tk.Toplevel(self.master)
        rules_win.title("Правила игры")
        rules_win.geometry("400x300")
        rules_win.resizable(False, False)

        text = tk.Text(rules_win, wrap=tk.WORD, font=("Arial", 10))
        text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        rules = """
        Правила игры «21 очко» (упрощённая версия):

        • Используется колода из 52 карт.
        • Достоинства: 2–9 — по номиналу, T/J/Q/K — 10 очков, A — 11 очков.
        • Игрок и крупье получают по две карты. Одна карта крупье закрыта.
        • Игрок может брать дополнительные карты (Hit) или остановиться (Stand).
        • Крупье берёт карты, пока его сумма ≤10 (по условию исходной программы).
        • Если у игрока или крупье сумма >21 — перебор и проигрыш.
        • Побеждает тот, у кого сумма ближе к 21, но не больше.
        • При равенстве — ничья.

        Удачи!
        """
        text.insert(tk.END, rules)
        text.config(state=tk.DISABLED)

#запуск стартого окна
def main():
    root = tk.Tk()
    root.withdraw()                # прячем главное окно
    start_win = tk.Toplevel(root)  # стартовое окно
    StartWindow(start_win)
    root.mainloop() #запуск цикла обработки событий

#ЛОГИРОВАНИЕ
class GameLogger:
    def __init__(self, log_file="blackjack_log.json"):#принимает имя файла
        self.log_file = log_file
        # создание файла если его нет
        if not os.path.exists(log_file):
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write('')

    #формирование записи в формате json
    def log(self, event_type, details):
        record = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type, #тип события
            "details": details #словарь с доп инфой
        }
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

# создание глобального логгера
logger = GameLogger()

# сохранение оригинальных методов
original_hit = GameWindow.hit
original_stand = GameWindow.stand
original_new_game = GameWindow.new_game
original_end_game = GameWindow.end_game

#логирование взятия карты
def logged_hit(self):
        logger.log("hit", {
            "player": self.game.player_name,
            "player_hand_before": [format_card(c) for c in self.game.player_hand],
            "player_score_before": count_score(self.game.player_hand)
        })
        original_hit(self)
        logger.log("hit_after", {
            "player": self.game.player_name,
            "player_hand_after": [format_card(c) for c in self.game.player_hand],
            "player_score_after": count_score(self.game.player_hand),
            "game_over": self.game.game_over
        })

#логирование остановки игры
def logged_stand(self):
        logger.log("stand", {
            "player": self.game.player_name,
            "player_hand": [format_card(c) for c in self.game.player_hand],
            "player_score": count_score(self.game.player_hand)
        })
        original_stand(self)

#логирование нового раунда
def logged_new_game(self):
    logger.log("new_game", {
        "player": self.game.player_name,
        "timestamp_start": datetime.now().isoformat()
    })
    original_new_game(self)

#логирование конца рануда
def logged_end_game(self):
    winner = self.game.get_winner()
    logger.log("game_over", {
        "player": self.game.player_name,
        "winner": winner,
        "player_hand": [format_card(c) for c in self.game.player_hand],
        "player_score": count_score(self.game.player_hand),
        "dealer_hand": [format_card(c) for c in self.game.dealer_hand],
        "dealer_score": count_score(self.game.dealer_hand)
    })
    original_end_game(self)

# подмена методов, автоматическое написание логов
GameWindow.hit = logged_hit
GameWindow.stand = logged_stand
GameWindow.new_game = logged_new_game
GameWindow.end_game = logged_end_game

# Дополнительно логируем начало сессии при создании GameWindow
original_init = GameWindow.__init__
def logged_init(self, master, player_name):
    logger.log("session_start", {"player": player_name}) #запись стартка с именем игрока 
    original_init(self, master, player_name)
GameWindow.__init__ = logged_init


main()