def get_bonus(utility_name,active_utils):
    if utility_name in active_utils.keys():
        return active_utils[utility_name].get_bonus()
    else:
        return 0