from PyInquirer import prompt
from gospel_message import gospel_message


def main():
    # Variables
    exit = False
    back = 'Go back to the menu'

    menu_gospel = 'What is the Gospel?'
    menu_heaven_or_hell = 'Heaven or Hell, where will you spend eternity?'
    menu_exit = 'exit'

    while exit != True:
        # Menu
        questions_menu = [
            {
                'type': 'list',
                'name': 'menu',
                'message': 'Menu:',
                'choices':
                    [
                        menu_gospel,
                        # menu_heaven_or_hell,
                        menu_exit,
                    ],
            },
        ]

        answer_menu = prompt(questions_menu)

        if answer_menu['menu'] == menu_exit:
            exit = True

        if answer_menu['menu'] == menu_gospel:
            print(gospel_message)
            questions_gospel = [
                {
                    'type': 'confirm',
                    'name': 'gospel',
                    'message': back,
                    'default': True,
                },
            ]

            answer_gospel = prompt(questions_gospel)

    print('For more info, go to CodeForFaith.com')


if __name__ == '__main__':
    main()
