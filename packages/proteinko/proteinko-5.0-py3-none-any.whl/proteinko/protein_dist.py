import numpy as np
from proteinko.utils import pdf


def model_distribution(sequence: str, encoding_scheme: dict, overlap_distance: int = 2,
                       sigma: float = 0.4, sampling_points: int = None):
    scaling_factor = 40
    sequence = sequence.upper()
    dist_vector = np.zeros(scaling_factor*len(sequence)+2*overlap_distance*scaling_factor)
    for i, aa in enumerate(sequence):
        try:
            value = encoding_scheme[aa]
        except KeyError:
            msg = 'Unrecognized amino acid: {}'.format(aa)
            raise KeyError(msg)
        x = np.linspace(-2.3263, 2.3263, (2*overlap_distance+1)*scaling_factor)
        aa_dist = pdf(x, sigma) * value
        dist_vector[int(i*scaling_factor):int((i+(2*overlap_distance+1))*scaling_factor)] += aa_dist
    dist_vector = dist_vector[overlap_distance*scaling_factor:-overlap_distance*scaling_factor]
    if sampling_points:
        sample_vector, offset = [], 0
        step = int(len(dist_vector) / sampling_points)
        for i in range(sampling_points):
            sample_tick = dist_vector[offset]
            offset += step
            sample_vector.append(sample_tick)
        dist_vector = np.array(sample_vector)
    return dist_vector


def encode_sequence(sequence: str, encoding_scheme: dict):
    encoded_sequence = []
    for aa in sequence:
        try:
            value = encoding_scheme[aa]
        except KeyError:
            msg = 'Unrecognized amino acid: {}'.format(aa)
            raise KeyError(msg)
        encoded_sequence.append(value)
    return np.array(encoded_sequence)
