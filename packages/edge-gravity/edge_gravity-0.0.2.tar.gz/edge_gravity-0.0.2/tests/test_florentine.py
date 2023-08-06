import networkx as nx
from edge_gravity import edge_gravity
import pytest


@pytest.fixture
def florentine_network():
    florentine_family = nx.generators.social.florentine_families_graph()

    new_g = nx.DiGraph()
    for node in florentine_family.nodes():
        new_g.add_node(node)

    for u, v in florentine_family.edges():
        new_g.add_edge(u, v)
        new_g.add_edge(v, u)

    florentine_family = new_g

    return florentine_family


def test_florentine_k_15(florentine_network):

    kstar_found, results = edge_gravity(florentine_network, k=15)
    results = results.most_common(40)

    assert kstar_found == False

    exp_results = set([
        (("Bischeri", "Guadagni"), 727),
        (("Guadagni", "Bischeri"), 717),
        (("Strozzi", "Ridolfi"), 677),
        (("Ridolfi", "Strozzi"), 676),
        (("Barbadori", "Castellani"), 573),
        (("Castellani", "Barbadori"), 562),
        (("Bischeri", "Peruzzi"), 543),
        (("Medici", "Barbadori"), 526),
        (("Peruzzi", "Bischeri"), 525),
        (("Guadagni", "Tornabuoni"), 518),
        (("Barbadori", "Medici"), 515),
        (("Tornabuoni", "Guadagni"), 506),
        (("Tornabuoni", "Ridolfi"), 486),
        (("Ridolfi", "Tornabuoni"), 485),
        (("Castellani", "Peruzzi"), 482),
        (("Peruzzi", "Castellani"), 472),
        (("Castellani", "Strozzi"), 471),
        (("Strozzi", "Castellani"), 470),
        (("Tornabuoni", "Medici"), 455),
        (("Medici", "Tornabuoni"), 444),
        (("Strozzi", "Bischeri"), 442),
        (("Peruzzi", "Strozzi"), 441),
        (("Albizzi", "Guadagni"), 436),
        (("Guadagni", "Albizzi"), 434),
        (("Ridolfi", "Medici"), 416),
        (("Bischeri", "Strozzi"), 414),
        (("Medici", "Ridolfi"), 414),
        (("Strozzi", "Peruzzi"), 413),
        (("Medici", "Albizzi"), 398),
        (("Albizzi", "Medici"), 396),
        (("Medici", "Salviati"), 334),
        (("Salviati", "Medici"), 334),
        (("Albizzi", "Ginori"), 196),
        (("Guadagni", "Lamberteschi"), 196),
        (("Lamberteschi", "Guadagni"), 196),
        (("Ginori", "Albizzi"), 196),
        (("Medici", "Acciaiuoli"), 168),
        (("Salviati", "Pazzi"), 168),
        (("Acciaiuoli", "Medici"), 168),
        (("Pazzi", "Salviati"), 168),
    ])

    assert set(results) == exp_results


def test_find_correct_k(florentine_network):
    # correct k according to Paper is 33

    k_star, _ = edge_gravity(florentine_network, k=32)
    assert k_star is False

    # kstar only is known if kstar + 1 is calculated
    k_star, _ = edge_gravity(florentine_network, k=33)
    assert k_star is False

    k_star, _ = edge_gravity(florentine_network, k=34)
    assert k_star == 33
