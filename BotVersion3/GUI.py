import tkinter as tk
from tkinter import scrolledtext

class ChatGUI(tk.Tk):
    def __init__(self, bot):
        super().__init__()

        self.title("Chat GUI")

        # Blue area: Chatbox with a scrolling feature
        self.chatbox = scrolledtext.ScrolledText(self, bg="lightskyblue3", fg="white", wrap=tk.WORD)
        self.chatbox.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        self.chatbox.tag_config("color1", foreground="firebrick1")
        self.chatbox.tag_config("color2", foreground="midnightblue")

        # Input area like a phone's texting app
        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(pady=10, padx=20, fill=tk.X, expand=True)

        self.user_input = tk.Entry(self.entry_frame)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.user_input.bind('<Return>', self.send_message)

        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        # Red area: Buttons with outside functionality
        self.button_frame = tk.Frame(self, bg="steelblue3")
        self.button_frame.pack(pady=10, padx=20, fill=tk.X, expand=True)

        self.button1 = tk.Button(self.button_frame, text="End Chat", command=self.end_convo)
        self.button1.pack(side=tk.LEFT, padx=5)

        self.button2 = tk.Button(self.button_frame, text="Button 2", command=self.some_function)
        self.button2.pack(side=tk.LEFT, padx=5)

        self.button3 = tk.Button(self.button_frame, text="Button 3", command=self.some_function)
        self.button3.pack(side=tk.LEFT, padx=5)

        # Info printed out below the red buttons
        self.info_label = tk.Label(self, text="Information will be printed here.")
        self.info_label.pack(pady=10, padx=20)

        self.last_user_message = ""
        self.bot = bot

    def send_message(self, event=None):
        message = self.user_input.get()
        if not message.strip():
            return  # Do nothing if the message is empty

        # Here, you can have conditions to check the ID of the message
        # and change the color accordingly.
        self.chatbox.config(state=tk.NORMAL)
        self.chatbox.insert(tk.END, f"You: {message}" + '\n', "color1")
        self.chatbox.config(state=tk.DISABLED)
        self.user_input.delete(0, tk.END)
        self.last_user_message = message
        self.get_response()

    #get response from the bot
    def get_response(self):
        message = self.bot.respond_to_input(self.last_user_message)
        if not message.strip():
            return  # Do nothing if the message is empty

        self.chatbox.config(state=tk.NORMAL)
        self.chatbox.insert(tk.END, f"{self.bot.name}: {message}" + '\n', "color2")
        self.chatbox.config(state=tk.DISABLED)

    def some_function(self):
        # Example function. You can modify this to do whatever you want.
        self.info_label.config(text="A button was pressed!")

    def end_convo(self):
        self.bot.to_lt_memory()

        self.chatbox.config(state=tk.NORMAL)  # Make the chatbox editable
        self.chatbox.delete(1.0, tk.END)      # Delete all content from the chatbox
        self.chatbox.config(state=tk.DISABLED)  # Make the chatbox non-editable again

if __name__ == "__main__":
    app = ChatGUI()
    app.mainloop()
