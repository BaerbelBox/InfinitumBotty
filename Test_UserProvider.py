from FaustBot.Model.UserProvider import UserProvider

user = UserProvider()
user.add_characters("Bla", 100)
user.set_active("Bla")
user.set_active("Mah")
print(user.get_characters("Bla"))
print(user.get_activity("Bla"))
print(user.get_characters("Blubb"))
print(user.get_activity("Blubb"))
print(user.get_characters("Mah"))
print(user.get_activity("Mah"))
