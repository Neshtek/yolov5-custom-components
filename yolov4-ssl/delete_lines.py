for i in range(797):
    with open(r"C:\\Users\\neela\\Documents\\yolov4\\text\\frame%d.txt" % i, 'r+') as fp:
        lines = fp.readlines()
        fp.seek(0)
        fp.truncate()
        for number, line in enumerate(lines):
            if number not in range(13):
                fp.write(line)