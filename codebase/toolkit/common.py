def template(i, o, d):
    """i.format(d)

    Args:
        i (str): input file path
        o （str): output file path
        d (dict):
    """
    with open(i, "r") as i:
        with open(o, "w") as o:
            o.write(
                i.read().format(**d)
            )