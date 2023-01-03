import csv


def parse(csv_path, ban_reason):
    result = ""
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',');
        line_index = 0
        for row in csv_reader:
            if line_index > 0:
                result = result + '/ban {username} {reason}\n'.format(username=row[0], reason=ban_reason)
            line_index = line_index + 1
    return result
