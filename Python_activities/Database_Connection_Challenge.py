from control import control


class main():
    def __init__(self):
        self.running = True

    def run(self):
        while self.running:
            print('============================')
            print('simple database application (CRUD)')
            print('============================')

            try:
                result = int(input('1. Create Student\n2. View Student\n3. Update Student\n4. Delete Student\n5. Exit\n'))

                match result:
                    case 1:
                        id = input('Enter student id: ')
                        name = input('Enter student name: ')
                        course = input('Enter student course: ')

                        cl = control(id, name, course)
                        cl.Create_students()

                    case 2:
                        read = control()
                        read.Read_students()
                    case 3:
                        update = int(input('Enter student id to update: '))

                        u_name = input('Enter student name: ')
                        u_course = input('Enter student course: ')

                        upd = control(update,u_name,u_course)
                        upd.Update_students()
                    case 4:
                        delete = int(input('Enter student id to delete: '))

                        dele = control(delete)
                        dele.Delete_students()

                    case 5:
                        print('ending program')
                        self.running = False

            except Exception as e:
                print(e)
                print('choose only 1-5')


app = main()
app.run()


