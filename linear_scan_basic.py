edit_distance_nn = utils.nearest_neighbours_linear_scan(
    Data, Data, editdistance.eval, iterator_type='list')

l1_distance_nn = utils.nearest_neighbours_linear_scan(
    embeddings, embeddings, utils.l_1, iterator_type='numpy')

comparison = utils.compare_nearest_neighbours(
    Data, Data, editdistance.eval, edit_distance_nn, l1_distance_nn)
