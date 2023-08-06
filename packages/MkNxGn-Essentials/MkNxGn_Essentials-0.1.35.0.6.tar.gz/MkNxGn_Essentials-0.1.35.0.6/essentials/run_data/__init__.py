import datetime, sys

STRING = str
INT = int
FLOAT = float

class Run_Data(object):
    """
    For use with python files.

    Use this module to collect input arguments and other data about your file


    Example:
    `
    from essentials import run_data

    file_run_data = run_data.Run_Data()

    #Collect input aruments from the command line
    
    #  - Strings
    mode = file_run_data.add_arg(run_data.Default_Arg('mode', default='easy', description="Mode game you would like. Options: easy normal hard"))

    #  - Integer
    speed = file_run_data.add_arg(run_data.Default_Arg('speed', arg_type=run_data.INT, required=True, description="How fast you want the game to go."))

    #  - Float
    pixel_size = file_run_data.add_arg(run_data.Default_Arg('pixel_size', default=0.5, arg_type=run_data.FLOAT, description="What size you'd like the game to be"))
    
    #How long your file has been active
    print("You've been playing for:", file_run_data.up_time.seconds, "seconds")

    `
    """
    

    def __init__(self):
        self.args = {}
        self.start_time = datetime.datetime.now()
        if __name__ == "__main__":
            self.main_thread = True
        else:
            self.main_thread = False
        self.caller = sys.argv[0]
        self.raw_args = sys.argv
        if len(self.raw_args) > 1:
            self.compressed_args = " ".join(self.raw_args[1:]).replace(" --", "--")
        else:
            self.compressed_args = ""
        self.parsed_agrs = self.compressed_args.split("--")[1:]
        self.__collected__ = False
        
    def add_arg(self, default_arg):
        if default_arg.name in self.args:
            raise NameError("The argument name is already present.")
        self.args[default_arg.name] = default_arg
        self.__collect__(default_arg)
        return default_arg.value

    @property
    def up_time(self):
        return datetime.datetime.now() - self.start_time


    def __collect__(self, arg):
        parsed = False
        for value in self.parsed_agrs:
            if arg.name + "=" in value:
                try:
                    arg.value = arg.type(value.split("=")[1])
                    parsed = True
                except:
                    pass
        if parsed == False:
            if arg.required == True and arg.default == None:
                print("Argument '" + arg.name + "' is a required " + arg.arg_type_string)
                print("Use --" + arg.name + "=[VALUE]", "to set this argument\n")
                if arg.description != "":
                    print(arg.name, "description:", arg.description)
                exit()
            else:
                arg.value = arg.default
        else:
            if len(arg.options) > 0 and arg.value not in arg.options:
                print("Argument '" + arg.name + "' is a required " + arg.arg_type_string)
                print("Use --" + arg.name + "=[VALUE]", "to set this argument\n")
                if arg.description != "":
                    print(arg.name, "description:", arg.description)
                print("Valid options for this argument include:")
                for item in arg.options:
                    print(item)
                exit()




class Default_Arg(object):
    def __init__(self, name, default=None, arg_type=STRING, description="", required=True, options=[]):
        self.name = name
        self.default = default
        self.required = required
        self.description = description
        self.type = arg_type
        self.value = default
        if arg_type == str:
            self.arg_type_string = "String"
        elif arg_type == int:
            self.arg_type_string = "Integer"
        elif arg_type == float:
            self.arg_type_string = "Float"
        else:
            self.arg_type_string = str(self.type)