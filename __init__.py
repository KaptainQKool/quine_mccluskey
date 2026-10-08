def quine_mccluskey(
    inputs: list[str],
    minterms: list[int],
    dont_cares: list[int]
) -> set[str]:
    n_inputs: int = len(inputs)

    # find all minterms in cube form
    implicants: set[str] = set()
    for m in minterms + dont_cares:
        implicants.add(cube_from_minterm(m, n_inputs))

    # sort implicants into groups based on how many 1s they have
    groups: list[set[str]] = []
    for i in implicants:
        c = i.count('1')
        while len(groups) <= c:
            groups.append(set())
        groups[c].add(i)

    # find prime implicants
    prime_implicants: set[str] = iteration(groups)

    # find essential prime implicants
    return essential_cubes(prime_implicants, minterms)


def cube_from_minterm(
    minterm: int,
    inputs: int
) -> str:
    cube_split: list[str] = []
    for i in range(inputs):
        cube_split.insert(0, str(minterm % 2))
        minterm = int(minterm / 2)
    return ''.join(cube_split)


def iteration(
    groups: list[set[str]]
) -> set[str]:
    out_groups: list[set[str]] = []
    used_cubes: set[str] = set()
    unused_cubes: set[str] = set()

    for g in groups:
        for c in g:
            unused_cubes.add(c)
    
    for i in range(0, len(groups)-1):
        new_group: set[str] = set()
        for j in groups[i]:
            for k in groups[i+1]:
                diff_index: int = diff(j, k)
                if matching_literals(j, k) and diff_index >= 0:
                    new_cube_split: list[str] = [c for c in j]
                    new_cube_split[diff_index] = 'X'
                    new_cube: str = ''.join(new_cube_split)
                    new_group.add(new_cube)
                    used_cubes |= {j, k}
        out_groups.append(new_group)
    unused_cubes -= used_cubes
    
    if any(out_groups):
        unused_cubes |= iteration(out_groups)
    return unused_cubes


def matching_literals(
    a: str,
    b: str
) -> bool:
    if len(a) != len(b):
        return False
    return not any([(a[i] == 'X') != (b[i] == 'X') for i in range(len(a))])


def diff(
    a: str,
    b: str
) -> int:
    if len(a) != len(b):
        return -1

    index: int = 0
    found: bool = False
    for i in range(len(a)):
        if a[i] != b[i]:
            if found:
                return -1
            index = i
            found = True

    return index


def essential_cubes(
    cubes: set[str],
    minterms: list[int]
) -> set[str]:
    out_cubes: set[str] = set()
    
    cover_chart: dict[str, set[int]] = {}
    for c in cubes:
        cover_chart |= {c: minterms_from_cube(c, minterms)}
    
    while any(cover_chart.values()):
        max_uncovered_cube: str = ""
        max_uncovered_minterms: set[int] = set()
        max_n_uncovered_minterms: int = 0
        for k, v in cover_chart.items():
            n_uncovered_minterms: int = len(v)
            if n_uncovered_minterms >= max_n_uncovered_minterms:
                max_uncovered_cube = k
                max_uncovered_minterms = v.copy()
                max_n_uncovered_minterms = n_uncovered_minterms

        out_cubes.add(max_uncovered_cube)
        for v in cover_chart.values():
            v -= max_uncovered_minterms

    return out_cubes


def minterms_from_cube(
    cube: str,
    minterms: list[int]
) -> set[int]:
    x_index: int = cube.find('X')
    if x_index >= 0:
        new_cube_0_split: list[str] = []
        new_cube_1_split: list[str] = []
        for c in cube:
            if c == 'X':
                new_cube_0_split.append('0')
                new_cube_1_split.append('1')
            else:
                new_cube_0_split.append(c)
                new_cube_1_split.append(c)
        return minterms_from_cube(''.join(new_cube_0_split), minterms) | minterms_from_cube(''.join(new_cube_1_split), minterms)
    else:
        out_minterms: set[int] = set()

        minterm: int = int(cube, 2)
        if minterm in minterms:
            out_minterms.add(minterm)
        
        return out_minterms


if __name__ == '__main__':
    # test
    # print(quine_mccluskey(['A', 'B', 'C', 'D', 'E', 'F'], [18, 30, 51], [19, 50]))
    
    # bhd converter
    print('D0')
    print(quine_mccluskey(
        ['W3', 'W2', 'W1', 'W0'], [1, 4, 11, 13], []
    ))
    print()
    
    print('D1')
    print(quine_mccluskey(
        ['W3', 'W2', 'W1', 'W0'], [5, 6, 11, 12, 14, 15], []
    ))
    print()
    
    print('D2')
    print(quine_mccluskey(
        ['W3', 'W2', 'W1', 'W0'], [2, 12, 14, 15], []
    ))
    print()
    
    print('D3')
    print(quine_mccluskey(
        ['W3', 'W2', 'W1', 'W0'], [1, 4, 7, 10, 15], [9]
    ))
    print()
    
    print('D4')
    print(quine_mccluskey(
        ['W3', 'W2', 'W1', 'W0'], [1, 3, 4, 5, 7, 9], []
    ))
    print()
    
    print('D5')
    print(quine_mccluskey(
        ['W3', 'W2', 'W1', 'W0'], [1, 2, 3, 7, 13], []
    ))
    print()
    
    print('D6')
    print(quine_mccluskey(
        ['W3', 'W2', 'W1', 'W0'], [0, 1, 7, 12], []
    ))
    print()