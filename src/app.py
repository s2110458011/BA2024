import customtkinter
from backend.controller import Controller


def main():
    #root = customtkinter.CTk()
    app = Controller()
    
    # run
    app.run()


if __name__ == "__main__":
    main()