class animal: #parent class

    alive = True

    def eat(self):
        print("this animal is eating")

    def slumber(self):
        print("this animal is sleeping")

class rabbit(animal): #child class
    alive = True

    def eat(self):
        print("this animal is eating")

    def sleep(self):
        print("this animal is sleeping")

class fish(animal): #child class
    pass

class hawk(animal): #child class
    pass

rabbit = rabbit()
fish = fish()
hawk = hawk()

print(rabbit.alive)
rabbit.sleep()
