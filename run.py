import os

if __name__ == "__main__":
    if os.getuid()==0:
        import interface
        interface.show()
    else:
        print ("Permission error...")
