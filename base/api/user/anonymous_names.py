from random import choice

def random_name():
    names = ['john','rock','sunny','jack','adam','andy','ziya','alex']
    random_choice = choice(names)
    print(random_choice)
    return random_choice


