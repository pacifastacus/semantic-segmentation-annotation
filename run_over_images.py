import glob

TEST_DIR='test_data/img/'

def sort_numbered_fname(e):
    import re
    match = re.search('([^0-9]*)([0-9]+)(.*)', e)
    num = int(match[2])
    return num

def get_images_list(dir, order_key=sort_numbered_fname):
    fname = glob.glob(dir + '*.jpg')
    fname.sort(key=order_key)
    return fname

def get_next_image(dir):
    file_list = get_images_list(dir, order_key=sort_numbered_fname)
    file_list.reverse()
    while(len(file_list)):
        yield file_list.pop()
