from doctest import master
import common as cf

if __name__ == "__main__":
    cf.delete_old_crawler()
    cf.update_categories()