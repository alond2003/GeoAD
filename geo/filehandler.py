import zipfile
import os


def get_points_from_file(path, temp_folder_path="temp_ggb"):
    """Return a list of (name,x,y) from a .ggb file"""

    # check file extension
    if not path.endswith(".ggb"):
        raise Exception(f"file type for file {path} is not supported. use .ggb instead")

    # exctract files from ggb file (actually zip)
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(temp_folder_path)

    # read main file from unziped folder
    with open(os.path.join(temp_folder_path, "geogebra.xml"), "r") as f:
        lines = f.readlines()

    # create a list of point tags
    point_tags = []
    is_inside_point_tag = False
    for line in lines:
        line = " ".join(line.strip().split())
        if line.startswith('<element type="point"'):
            is_inside_point_tag = True
            point_tags.append("")
        if is_inside_point_tag:
            point_tags[-1] += line + "\n"
            if line.startswith("</element>"):
                is_inside_point_tag = False

    # create list of points from tags
    points = []
    # points[i] = (name,x,y)

    for point_tag in point_tags:
        name = point_tag.split("\n")[0].split('label="')[1].split('"')[0]
        x, y = None, None
        for line in point_tag.split("\n"):
            if line.startswith("<coords"):
                x = float(line.split('x="')[1].split('"')[0])
                y = float(line.split('y="')[1].split('"')[0])
                break
        points.append((name, x, y))

    # remove temp_folder
    for filename in os.listdir(temp_folder_path):
        os.remove(os.path.join(temp_folder_path, filename))
    os.rmdir(temp_folder_path)

    # return the sorted points' list
    return sorted(points)


def print_points_from_file(
    path=r"C:\Users\alond\Documents\School\AvodatGemer\AvodatGemerCode\ggb_test\test.ggb",
    temp_folder_path="temp_ggb",
):
    """Print Point names, xs and ys"""
    res = get_points_from_file(path, temp_folder_path)

    names = [name for name, *_ in res]
    xs = [round(x, 2) for _, x, _ in res]
    ys = [round(y, 2) for *_, y in res]
    xs = [int(x) if x.is_integer() else x for x in xs]
    ys = [int(y) if y.is_integer() else y for y in ys]
    print(f"h.ps(\"{''.join(names)}\",{xs},{ys})")
