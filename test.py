

class test2:
    def __init__(self, name):
        self.name = name
        self.name = "test2"

    def run(self):
        print(f"Running {self.name}")
        
class test1:
    def __init__(self, name):
        # self.name = "test1"
        self.name = "aaaaaaaaaaa"
        self.test = test2(name)

    def run(self):
        print(f"Running {self.name}")
        
if __name__ == "__main__":
    t1 = test1("test1")
    print(t1.name)