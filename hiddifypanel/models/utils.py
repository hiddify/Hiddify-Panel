from hiddifypanel import hutils


def fill_username(model) -> None:
    minimum_username_length = 10
    if not model.username or len(model.username) < minimum_username_length:
        base_username = ''
        rand_str = ''
        if not model.name:
            base_username = hutils.utils.get_random_string(minimum_username_length, minimum_username_length)
            model.username = base_username + rand_str
            while not model.is_username_unique():
                rand_str = hutils.utils.get_random_string(minimum_username_length, minimum_username_length)
        else:
            # user actual name
            base_username = model.name.replace(' ', '_')
            if len(base_username) > minimum_username_length - 1:
                # check if the name is unique, if  it's not we add some random char to it
                model.username = base_username + rand_str
                while not model.is_username_unique():
                    rand_str = hutils.utils.get_random_string(2, 4)
            else:
                needed_length = minimum_username_length - len(base_username)
                rand_str = hutils.utils.get_random_string(needed_length, needed_length)
                model.username = base_username + rand_str
                while not model.is_username_unique():
                    rand_str = hutils.utils.get_random_string(needed_length, needed_length)


def fill_password(model) -> None:
    # TODO: hash the password
    if not model.password or len(model.password) < 16:
        base_passwd = hutils.utils.get_random_password()
        rand_str = ''
        # if passwd is duplicated, we create another one
        model.password = base_passwd + rand_str
        while not model.is_password_unique():
            rand_str = hutils.utils.get_random_password()