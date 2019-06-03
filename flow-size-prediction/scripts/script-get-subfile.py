import csv


file_path = '../../../datasets/Dataset-Unicauca-Version2-87Atts.csv'

FILE_SIZE = 10000
with open(file_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    rows = []
    for row in csv_reader:
        if line_count < FILE_SIZE:
            rows.append(row)
            line_count = line_count + 1
        else:
            # Escreve novo arquivo
            filename = 'unicauca{0}.csv'.format(FILE_SIZE)

            with open(filename, mode='w') as subfile:
                writer = csv.writer(subfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in rows:
                    writer.writerow(row)
            exit(0)
