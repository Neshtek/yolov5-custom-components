import os

for root, dirs, files in os.walk('text/'):
    # for d in ['RECYCLER', 'RECYCLED']:
    #     if d in dirs:
    #         dirs.remove(d)

    for file in files:
        text_path = os.path.join(root, file)
        img_file = file[:-4] + ".jpg"
        img_path = os.path.join('img/', img_file)
        # print(img_path)
        # print(text_path)
        
        try:
            if os.path.getsize(text_path) == 0:
                os.remove(img_path)
                os.remove(text_path)
        except WindowsError:
            continue