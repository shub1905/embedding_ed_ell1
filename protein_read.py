import sys


def read_file_protein(file_handle):
    header_line = file_handle.readline()
    proteins = []
    for line in file_handle:
        line = line.replace('\n', '')
        proteins.append(line.split('\t')[-1])
    return proteins


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '''usage: python protein_read.py file_name'''
        sys.exit(0)

    file_name = sys.argv[1]
    file_handle = open(file_name, 'r')
    proteins = read_file_protein(file_handle)
    print proteins[:5]
    file_handle.close()