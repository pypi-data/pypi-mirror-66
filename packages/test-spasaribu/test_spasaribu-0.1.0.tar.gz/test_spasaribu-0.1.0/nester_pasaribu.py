"""This is the "nester.py" module, and it provides on function called
print_lol() which prints lists that may or may nit include nested lists."""

def print_lol(the_list, level=0):

    """This function takes a positional argument called "the_list",
    which is any Python list (of, possibly, nested lists). Each data
    item in the provided list is (recursively) printed to the screen on
    its own line and indent each nested list whenever one is found."""

    for each_item in the_list :
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)
