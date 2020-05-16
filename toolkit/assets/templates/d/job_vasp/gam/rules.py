taskpernode = {
    'comet': 24,
    'localhost': 16,
    'eccle': 32,
    'haswell': 32,
    'irmik': 12,
    'knl': 16,  # OpenMP MPI hybrid, refer to training pptx, I've absolutely no idea,
    'nanaimo': 24
}[cluster]

if cluster == 'node':
    nnode = 1

ntask = taskpernode * nnode
