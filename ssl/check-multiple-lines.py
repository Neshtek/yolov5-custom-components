import os

for root, dirs, files in os.walk('text/'):
    # for d in ['RECYCLER', 'RECYCLED']:
    #     if d in dirs:
    #         dirs.remove(d)

    for file in files:
        file_path = os.path.join(root, file)
        try:
            count = len(open(file_path).readlines())
            if count > 1:
                print(file_path)
        except WindowsError:
            continue
