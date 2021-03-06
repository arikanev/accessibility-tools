import os

tables = []

for root, dir, files in os.walk('./tables/'):

    for table in files:

            tables.append(table.strip(".table"))


vids = []

for root, dir, files in os.walk('./vids/'):

    for vid in files:

        if vid.strip(".MOV") not in tables:

            vids.append(vid)


W22 = {1:1, 2:3, 3:5, 4:7}
# 1->1 2->3 3->5 4->7

for vid in vids:

    with open('./tables/reference.table', 'r') as r:

        for rline in r.readlines():

            if vid.strip(".MOV")+" " in rline:

                for l, i in W22.items():

                    if str(l) in rline.split('./')[1].replace("W22", ""):

                        print(l, rline.split('./')[1].replace("W22", ""))

                        with open('./tables/W22.table', 'r') as w:

                            with open('./tables/' + vid.strip(".MOV") + ".table", 'w') as t:

                                if os.stat('./tables/' + vid.strip(".MOV") + ".table").st_size == 0:

                                    t.write(str(0) + '. ' + 'START' + ' 0 - 5\n')

                                for idx, wline in enumerate(w.readlines()):

                                    t.write(str(idx + 1) + '. ' + wline.split()[i] + ' 0 - 5\n')
