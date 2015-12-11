import sys


def read_file_protein(file_name=None):
    if file_name == None:
        file_name = 'raw_data/UniProt.txt'

    file_handle = open(file_name, 'r')
    header_line = file_handle.readline()
    proteins = []
    for line in file_handle:
        line = line.replace('\n', '')
        proteins.append(line.split('\t')[-1])

    file_handle.close()
    return proteins


if __name__ == '__main__':
    file_name = None
    if len(sys.argv) < 2:
        file_name = 'raw_data/UniProt.txt'
    else:
        file_name = sys.argv[1]
    proteins = read_file_protein(None)
    print proteins
