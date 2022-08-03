import common as cf

if __name__ == "__main__":
    infinite = cf.get_infinite_mode()
    if infinite:
        cf.check_for_all_infinite_finished()
    cf.update_status()
    masters = cf.get_init_site()
    for master in masters:
        if master['is_infinite'] == 1 and infinite:
            cf.add_remove_infinite_categories(master['id'])
            print("add all categories with delete old")
        cf.find_match_categories(master['id'])