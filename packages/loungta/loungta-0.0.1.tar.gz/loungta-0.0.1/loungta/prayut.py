
class Loongtu:
    def __init__(self):
        self.name = 'Prayut'
        self.lastname = 'Chanocha'
        self.nickname = 'Loong tu'

    def WhoIAm(self):
        '''
        This is a function will show the name.
        '''
        print('My name is: {}'.format(self.name))
        print('My lastname is: {}'.format(self.lastname))
        print('My nickname is: {}'.format(self.nickname))
    
    def email(self):
        return 'email: {}.{}@gmail.com'.format(self.name.lower(),self.lastname.lower())

    @property
    def email_decorator(self):
        return 'email: {}.{}@gmail.com'.format(self.name.lower(),self.lastname.lower())

    def thainame(self):
        print('ประยุทธ์ จันทร์โอชา')
        return 'ประยุทธ์ จันทร์โอชา'

    def __str__(self):
        return 'This is a Loongtu class'

if __name__ == '__main__':
    # Create instance objects.
    loongtu = Loongtu()
    print(loongtu.name)               # Display attribute value.
    print(loongtu.lastname)
    print(loongtu.nickname)
    print("--------------")
    loongtu.thainame()                # Display in thai name
    print("--------------")

    # Callling from __str__ dunder
    print(loongtu)
    print("--------------")

    # Callling from WhoIAm method function
    loongtu.WhoIAm()
    print("--------------")

    # Callling from email method function
    print(loongtu.email())
    print("--------------")

    # Calling with @property decorator
    print(loongtu.email_decorator)

    # Create instance objects. for calling same class
    mypaa = Loongtu()
    # Adding new attribute values.
    mypaa.name = 'Somsri'
    mypaa.lastname = 'Konthai'
    mypaa.nickname = 'Sri'
    print("--------------")
    print(mypaa.name)                 # Display New adding value
    print(mypaa.lastname)
    print(mypaa.nickname)