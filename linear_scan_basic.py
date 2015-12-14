import data_generation
import psi_generator
import editdistance
import utils
import numpy

Data = data_generation.read_file_protein()
embeddings = psi_generator.driver_embeddings(Data, alphabet_size=22)

edit_distance_nn = utils.nearest_neighbours_linear_scan(
    Data, Data, editdistance.eval, iterator_type='list')

l1_distance_nn = utils.nearest_neighbours_linear_scan(
    embeddings, embeddings, utils.l_1, iterator_type='numpy')

comparison = utils.compare_nearest_neighbours(
    Data, Data, editdistance.eval, edit_distance_nn, l1_distance_nn, print_summary=True, file_name='genes_big.png')
