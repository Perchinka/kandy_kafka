from kandy_kafka.bootstrap import Bootstrap
from kandy_kafka.gui.gui import GUI

def main():
    # TODO: Read cli arguments and update config
    Bootstrap()()

    gui = GUI()
    gui.run()
    
if __name__ == "__main__":
    main()