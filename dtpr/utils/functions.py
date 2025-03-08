""" Miscelaneous """
import os
import ROOT as r
from types import LambdaType
import math
import warnings

r.gStyle.SetOptStat(0)


# Make Iterators for when we want to iterate over different subdetectors
wheels = range(-2, 3)
sectors = range(1, 15)
stations = range(1, 5)
superlayers = range(1, 4)

_noDelete = {"lines": []}


def color_msg(msg, color="none", indentLevel=-1, return_str=False, bold=False, underline=False, bkg_color="none"):
    """
    Prints a message with ANSI coding so it can be printed with colors.

    Args:
        msg (str): The message to print.
        color (str): The color to use for the message. Default is "none".
        indentLevel (int): The level of indentation. Default is -1.
        return_str (bool): If True, returns the formatted message as a string. Default is False.
        bold (bool): If True, makes the text bold. Default is False.
        underline (bool): If True, underlines the text. Default is False.

    Returns:
        str: The formatted message if return_str is True.
    """
    style_digit = "0"
    if bold and underline:
        style_digit = "1;4"
    elif bold:
        style_digit = "1"
    elif underline:
        style_digit = "4"

    colors = ["black", "red", "green", "yellow", "blue", "purple", "cyan", "white"]
    font_colors = {color: f";{30 + i}" for i, color in enumerate(colors)}
    background_colors = {color: f";{40 + i}" for i, color in enumerate(colors)}
    font_colors["none"] = ""
    background_colors["none"] = ""

    try:
        ansi_code = f"{style_digit}{font_colors[color]}{background_colors[bkg_color]}m"
    except KeyError:
        ansi_code = f"{style_digit}{font_colors['none']}{background_colors['none']}m"

    indentStr = ""
    if indentLevel == 0:
        indentStr = ">>"
    if indentLevel == 1:
        indentStr = "+"
    if indentLevel == 2:
        indentStr = "*"
    if indentLevel == 3:
        indentStr = "-->"
    if indentLevel >= 4:
        indentStr = "-"

    formatted_msg = "\033[%s%s %s \033[0m" % (
        ansi_code,
        "  " * indentLevel + indentStr,
        msg,
    )

    if return_str:
        return formatted_msg
    else:
        print(formatted_msg)


def warning_handler(message, category, filename, lineno, file=None, line=None):
    """
    Handles warnings by printing them with color formatting.

    Args:
        message (str): The warning message.
        category (Warning): The category of the warning.
        filename (str): The name of the file where the warning occurred.
        lineno (int): The line number where the warning occurred.
        file (file object, optional): The file object. Default is None.
        line (str, optional): The line of code where the warning occurred. Default is None.
    """
    print(
        "".join(
            [
                color_msg(
                    f"{category.__name__} in:",
                    color="yellow",
                    return_str=True,
                    indentLevel=-1,
                ),
                color_msg(
                    f"{filename}-{lineno} :",
                    color="purple",
                    return_str=True,
                    indentLevel=-1,
                ),
                color_msg(f"{message}", return_str=True, indentLevel=-1),
            ]
        )
    )


def error_handler(exc_type, exc_value, exc_traceback):
    """
    Handles errors by printing them with color formatting.

    Args:
        exc_type (type): The type of the exception.
        exc_value (Exception): The exception instance.
        exc_traceback (traceback): The traceback object.
    """
    import traceback

    print(
        "".join(
            [
                color_msg(
                    f"{exc_type.__name__}:",
                    color="red",
                    return_str=True,
                    indentLevel=-1,
                ),
                color_msg(
                    f"{exc_value}", color="yellow", return_str=True, indentLevel=-1
                ),
                color_msg(
                    (
                        "Traceback (most recent call last):"
                        + "".join(traceback.format_tb(exc_traceback))
                        if exc_traceback
                        else ""
                    ),
                    return_str=True,
                    indentLevel=-1,
                ),  # [-2:]
            ]
        )
    )

def flatten(lst):
    """
    Flattens a nested list. If the input is not a list, returns the single value as a list.

    Args:
        lst (list): The nested list to flatten.

    Returns:
        list: The flattened list or the single value as a list.
    """
    if not isinstance(lst, list):
        return [lst]
    
    result = []
    for i in lst:
        if isinstance(i, list):
            result.extend(flatten(i))
        else:
            result.append(i)
    return result

def wrap_lambda(func):
    if isinstance(func, LambdaType) and func.__name__ == "<lambda>":
        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapped_func
    return func

def create_outfolder(outname):
    """
    Creates an output directory if it does not exist.

    Args:
        outname (str): The path of the output directory.
    """
    if not (os.path.exists(outname)):
        os.system("mkdir -p %s" % outname)

def save_mpl_canvas(fig, name, path = "./results", dpi=500):
    """
    Save the given matplotlib figure to the specified path in SVG format.

    Parameters:
    fig (matplotlib.figure.Figure): The figure to save.
    name (str): The name of the file (without extension).
    path (str): The directory where the file will be saved. Default is "./results".
    """
    if not os.path.exists(path):
        os.system("mkdir -p %s"%(path))
    fig.savefig(path + "/" + name+".svg", dpi=dpi)
    return

def get_unique_locs(particles, loc_ids=["wh", "sc", "st"]):
    """
    Returns the unique locations of the specified particle types.

    Args:
        reader (object): The reader object containing the specified particle types.
        particle_types (list): The list of particle types to consider.
        loc_ids (list, optional): The location IDs. Default is ["wh", "sc", "st"].

    Returns:
        list: The unique locations of the specified particle types in tuple format.
    """
    locs = []

    if particles:
        for particle in particles:
            try:
                locs.append(tuple([getattr(particle, loc_id) for loc_id in loc_ids]))
            except AttributeError as er:
                raise ValueError(f"Location Id attribute not found in particle object: {er}")

    return set(locs)

def get_best_matches(reader, station=1):
    """
    Returns the best matching segments for each generator muon.

    Args:
        reader (object): The reader object containing generator muons.
        station (int): The station number. Default is 1.

    Returns:
        list: The best matching segments.
    """

    genmuons = reader.genmuons

    bestMatches = [None for igm in range(len(genmuons))]

    # This is what's done in Jaime's code: https://github.com/jaimeleonh/DTNtuples/blob/unifiedPerf/test/DTNtupleTPGSimAnalyzer_Efficiency.C#L181-L208
    # Basically: get the best matching segment to a generator muon per MB chamber

    # color_msg(f"[FUNCTIONS::GET_BEST_MATCHES] Debugging with station {station}", color = "red", indentLevel = 0)
    for igm, gm in enumerate(genmuons):
        # color_msg(f"[FUNCTIONS::GET_BEST_MATCHES] igm {igm}", indentLevel = 1)
        # gm.summarize(indentLevel = 2)
        for bestMatch in gm.matches:
            if bestMatch.st == station:
                bestMatches[igm] = bestMatch

    # Remove those that are None which are simply dummy values
    bestMatches = filter(lambda key: key is not None, bestMatches)
    return bestMatches

def deltaPhi(phi1, phi2):
    """
    Calculates the difference in phi between two angles.

    Args:
        phi1 (float): The first angle in radians.
        phi2 (float): The second angle in radians.

    Returns:
        float: The difference in phi.
    """
    res = phi1 - phi2
    while res > math.pi:
        res -= 2 * math.pi
    while res <= -math.pi:
        res += 2 * math.pi
    return res


def deltaR(p1, p2):
    """
    Calculates the delta R between two particles.

    Args:
        p1 (object): The first particle with attributes eta and phi.
        p2 (object): The second particle with attributes eta and phi.

    Returns:
        float: The delta R value.
    """
    dEta = abs(p1.eta - p2.eta)
    dPhi = deltaPhi(p1.phi, p2.phi)
    return math.sqrt(dEta * dEta + dPhi * dPhi)


def phiConv(phi):
    """
    Converts a phi value.

    Args:
        phi (float): The phi value to convert.

    Returns:
        float: The converted phi value.
    """
    return 0.5 * phi / 65536.0
