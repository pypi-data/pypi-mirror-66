import time


class Dump(object):

    def __init__(self, dump_file=None):
        if dump_file is None:
            self.file_name = "dump_file_{}.log".format(self.get_time_stamp())
        else:
            self.file_name = dump_file
        print("Dump file: {}".format(self.file_name))
        self.file_handler = open(self.file_name, "a")
        self.init_head()

    def __del__(self):
        self.file_handler.close()

    def init_head(self):
        self.dump("Name", "Operation", "Value", "Expression")

    @staticmethod
    def get_time_stamp():
        return time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))

    def log(self, log_content):
        self.file_handler.write(log_content)

    def dump(self, name=None, operation=None, value=None, expression=None, ):
        name, operation, value, expression = self.format_log(name, operation, value, expression)
        context = "{} {} {} {}\n".format(name, operation, value, expression)
        self.file_handler.write(context)

    def format_log(self, name, operation, value, expression):
        name = self.format_(name, 30)
        operation = self.format_(operation, 10)
        expression = self.format_(expression, 50)
        value = self.format_(value, 15)
        return name, operation, value, expression

    def format_(self, string_, max_len):
        if type(string_) == int:
            temp = "0x{:x}".format(string_)
            new_string = "{}{}".format(temp, " "*(max_len-len(temp)))
        else:
            if string_ is not None:
                max_len = len(string_) if len(string_) > max_len else max_len
                new_string = "{}{}".format(string_, " " * (max_len - len(string_)))
            else:
                new_string = " "*max_len
        return new_string
