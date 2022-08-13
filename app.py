from tkinter import *
import webbrowser
from functools import partial
from tkHyperlinkManager import HyperlinkManager
from chatbot import response, recommend, predict_int, predict
import csv

BG_GRAY = '#a8cfed'
BG_COLOR = '#638ca6'
TEXT_COLOR = '#B1D0E0'
FONT = "Calibri 14"
FONT_BOLD = "Calibri 14 bold"


class ChatApplication():

    def __init__(self):
        self.window = Tk()
        self.name = ''
        self.msg = ''
        self.int = ''
        self.emo = ''
        self.int_prob = 0.0
        self.emo_prob = 0.0
        self._setup_main_window()

    def _setup_main_window(self):
        self.window.title("Chat System Project")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=700, height=600, bg=BG_COLOR)

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="MoodBot: A Friendly Chatbot", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1, relheight=0.07)

        # tiny divider

        label1 = Label(self.window, bg=BG_GRAY,
                       text="Chat", font=FONT_BOLD, pady=10, relief='solid', borderwidth=4)
        label1.place(relwidth=0.6, relheight=0.07, rely=0.08)

        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=0.6, rely=0.16, relheight=0.01)
        # text widget

        self.text_widget = Text(self.window, width=15, height=1, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5, wrap=WORD)
        self.text_widget.place(relheight=0.650, relwidth=0.6, rely=0.150)
        self.text_widget.configure(cursor="arrow", state=DISABLED)


        label2 = Label(self.window, bg=BG_GRAY,
                       text="Recommendations", font=FONT_BOLD, pady=10, relief='solid', borderwidth=4)
        label2.place(relx=0.6, relwidth=0.4, relheight=0.07, rely=0.08)

        self.text_widget2 = Text(self.window, width=15, height=1, bg=BG_COLOR, fg=TEXT_COLOR,
                                 font=FONT, padx=5, pady=5, wrap=WORD)
        self.text_widget2.place(relheight=0.650, relwidth=0.4, relx=0.6, rely=0.150)
        self.text_widget2.configure(cursor="arrow", state=DISABLED)

        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.800)

        # message entry box
        self.msg_entry = Entry(bottom_label, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="Enter", font=FONT_BOLD, width=20, bg='#996666',
                             command=lambda: self._on_enter_pressed(None), relief='solid', borderwidth=1)
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        if self.name == '':
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, f"BOT: Hello! I am MoodBot. You can type 'quit' to exit anytime.\n\n")
            self.text_widget.insert(END, f'BOT: Could you please first tell me your name?\n\n')
            self.text_widget.configure(state=DISABLED)

        text = ['Input Text', 'Intention', 'Probability', 'Emotion', 'Probability']
        self.save_res(text)

    def recommend_song(self, similar):
        self.text_widget2.configure(state=NORMAL)
        self.text_widget2.delete(1.0, END)

        self.text_widget2.insert(END, "\t    Top 5 Songs\n\n")
        hyperlink = HyperlinkManager(self.text_widget2)
        self.text_widget2.insert(INSERT, "1: ")
        self.text_widget2.insert(INSERT, f"{similar[0][0]}\n",
                                 hyperlink.add(partial(webbrowser.open, f"{similar[0][1]}")))
        self.text_widget2.insert(INSERT, "2: ")
        self.text_widget2.insert(INSERT, f"{similar[1][0]}\n",
                                 hyperlink.add(partial(webbrowser.open, f"{similar[1][1]}")))
        self.text_widget2.insert(INSERT, "3: ")
        self.text_widget2.insert(INSERT, f"{similar[2][0]}\n",
                                 hyperlink.add(partial(webbrowser.open, f"{similar[2][1]}")))
        self.text_widget2.insert(INSERT, "4: ")
        self.text_widget2.insert(INSERT, f"{similar[3][0]}\n",
                                 hyperlink.add(partial(webbrowser.open, f"{similar[3][1]}")))
        self.text_widget2.insert(INSERT, "5: ")
        self.text_widget2.insert(INSERT, f"{similar[4][0]}\n",
                                 hyperlink.add(partial(webbrowser.open, f"{similar[4][1]}")))
        self.text_widget2.insert(END, "\n\n\t   Similar Songs\n\n")
        self.text_widget2.insert(INSERT, "- ")
        self.text_widget2.insert(INSERT, f"{similar[5][0]}\n",
                                 hyperlink.add(partial(webbrowser.open, f"{similar[5][1]}")))
        self.text_widget2.insert(INSERT, "- ")
        self.text_widget2.insert(INSERT, f"{similar[6][0]}\n",
                                 hyperlink.add(partial(webbrowser.open, f"{similar[6][1]}")))
        self.text_widget2.insert(INSERT, "- ")
        self.text_widget2.insert(INSERT, f"{similar[7][0]}\n",
                                 hyperlink.add(partial(webbrowser.open, f"{similar[7][1]}")))
        self.text_widget2.insert(INSERT, "- ")
        self.text_widget2.insert(INSERT, f"{similar[8][0]}\n",
                                 hyperlink.add(partial(webbrowser.open, f"{similar[8][1]}")))
        self.text_widget2.insert(INSERT, "- ")
        self.text_widget2.insert(INSERT, f"{similar[9][0]}\n",
                                 hyperlink.add(partial(webbrowser.open, f"{similar[9][1]}")))

        self.text_widget2.configure(state=DISABLED)

    def _on_enter_pressed(self, event):
        self.msg = self.msg_entry.get()
        self._insert_message(self.msg, self.name)
        self.store_res()

    def save_text(self):
        text_file = open("test.txt", "w")
        text_file.write(self.text_widget.get(1.0, END))
        text_file.close()

    def save_res(self,text):
        res_file = open("test_res.csv", "a")
        writer = csv.writer(res_file)
        writer.writerow(text)

    def store_res(self):
        text = [self.msg, self.int, self.int_prob, self.emo, self.emo_prob]
        self.save_res(text)

    def _insert_message(self, msg, sender):
        if not msg:
            return

        if self.name == '':
            if not msg:
                return

            self.name = msg.upper()
            self.text_widget.configure(state=NORMAL)
            msg_bot = f'BOT: Nice to see you {self.name}! If you want to know what I can do, just feel free to ask me.\n\n'
            self.text_widget.insert(END, msg_bot)
            self.text_widget.configure(state=DISABLED)
            self.msg_entry.delete(0, END)
            return

        self.int,self.int_prob = predict_int(msg)
        self.emo,self.emo_prob = predict(msg)
        if self.int == 'goodbye' or self.int == 'courtesy_goodbye':
            self.msg_entry.delete(0, END)
            self.text_widget.configure(state=NORMAL)
            msg1 = f"{sender}: {msg}\n\n"
            self.text_widget.insert(END, msg1)
            msg_bot = f"BOT: Goodbye {self.name}! Remember to type 'quit' to exit.\n\n"
            self.text_widget.insert(END, msg_bot)
            self.text_widget.configure(state=DISABLED)
            self.msg_entry.delete(0, END)
            return

        if msg == 'quit':
            self.save_text()
            self.exit()

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        msg2 = f"BOT: {response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        x = recommend(msg)
        if x is not None:
            self.recommend_song(x)

        self.text_widget.see(END)
        # block2

    def run(self):
        self.window.mainloop()

    def exit(self):
        self.window.destroy()


if __name__ == "__main__":
    app = ChatApplication()
    app.run()