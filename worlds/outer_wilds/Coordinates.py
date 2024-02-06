from typing import List
from random import Random


two_point_coordinates = 6 * 5
three_point_coordinates = 6 * 5 * 4
four_point_coordinates = 6 * 5 * 4 * 3
five_point_coordinates = 6 * 5 * 4 * 3 * 2
six_point_coordinates = 6 * 5 * 4 * 3 * 2 * 1

total_possible_coordinates = (two_point_coordinates + three_point_coordinates + four_point_coordinates +
                              five_point_coordinates + six_point_coordinates)

# Some Nomai coordinates are nearly identical to English letters, namely: N, I/l and C
# To avoid even the miniscule chance of randomized coordinates resembling a bad word,
# we prevent those specific letter-shaped coordinates from being used.
# Since lists are not hashable, we have to use tuples here.
deny_list = {
    # 0 = Right, 1 = UpperRight, 2 = UpperLeft, 3 = Left, 4 = LowerLeft, 5 = LowerRight
    (4, 2, 5, 1),  # N
    (4, 2),  # I/l (left of center)
    (5, 1),  # I/l (right of center)
    (5, 4, 3, 2, 1)  # C
}


def generate_random_coordinates(random: Random) -> List[List[int]]:
    selections = [
        random.randint(0, total_possible_coordinates - 1),
        random.randint(0, total_possible_coordinates - 1),
        random.randint(0, total_possible_coordinates - 1),
    ]
    selected_coordinates = list(map(get_coordinate_for_number, selections))
    map(validate_coordinate, selected_coordinates)

    # if we hit the deny list, simply try again
    for c in selected_coordinates:
        if (tuple(c) in deny_list) or (tuple(reversed(c)) in deny_list):
            return generate_random_coordinates(random)
    return selected_coordinates


def validate_coordinate(coordinate: List[int]) -> None:
    assert len(coordinate) >= 2
    assert len(coordinate) <= 6
    assert len(set(coordinate)) == len(coordinate)


# Here, the number represents an index into the list of all possible coordinates of any length
def get_coordinate_for_number(coord_index: int) -> List[int]:
    assert coord_index < total_possible_coordinates

    if coord_index < two_point_coordinates:
        return get_coordinate_points_for_number(2, two_point_coordinates, coord_index)
    coord_index -= two_point_coordinates

    if coord_index < three_point_coordinates:
        return get_coordinate_points_for_number(3, three_point_coordinates, coord_index)
    coord_index -= three_point_coordinates

    if coord_index < four_point_coordinates:
        return get_coordinate_points_for_number(4, four_point_coordinates, coord_index)
    coord_index -= four_point_coordinates

    if coord_index < five_point_coordinates:
        return get_coordinate_points_for_number(5, five_point_coordinates, coord_index)
    coord_index -= five_point_coordinates

    return get_coordinate_points_for_number(6, six_point_coordinates, coord_index)


# Now the number represents an index into the list of all possible coordinates of one specific length
def get_coordinate_points_for_number(point_count: int, possible_coords: int, coord_index: int) -> List[int]:
    points_not_taken = [0, 1, 2, 3, 4, 5]
    coord_points = []
    bucket_size = possible_coords

    while len(coord_points) < point_count:
        bucket_size //= len(points_not_taken)
        point_choice = coord_index // bucket_size

        point_num = points_not_taken[point_choice]
        points_not_taken.remove(point_num)
        coord_points.append(point_num)

        coord_index %= bucket_size

    return coord_points
