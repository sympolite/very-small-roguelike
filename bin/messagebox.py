import tdl


class MessageBox:
    def __init__(self, console):
        self.console = console
        self.queue = []

    def add_to_queue(self, stringtuple):
        self.queue.append(stringtuple)

    def print_queue(self):
        if self.queue:
            for counter, stringtuple in enumerate(self.queue):
                self.console.draw_str(1, counter+1, stringtuple[0], stringtuple[1], stringtuple[2])
            self.queue = []

    def draw_msgbox(self):
        self.console.draw_rect(0, 0, None, None, None, fg=(255, 255, 255), bg=(32, 32, 32))

    def clear_message(self):
        for i in range(0, self.console.height-1):
            self.console.draw_str(1, i+1, " "*(self.console.width-1), fg=(255, 255, 255), bg=None)
