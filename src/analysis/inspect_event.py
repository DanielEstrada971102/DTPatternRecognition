import importlib
from dtpr.utils.functions import color_msg
from src.utils.config import RUN_CONFIG
from tqdm import tqdm

def inspect_event(
        inpath: str,
        maxfiles: int,
        event_number: int,
        debug: bool
    ):
    """
    Inspect a specific event from NTuples.

    Parameters:
    inpath (str): Path to the input folder containing the ntuples.
    outfolder (str): Path to the output folder where debug information will be saved.
    filter_type (str): Type of event filter to apply.
    maxfiles (int): Maximum number of files to process.
    event_number (int or str): The event number to inspect or a slice string indicating the slice, e.g. 1:10:2. Default is 0.
    debug (bool): If True, enables debug mode. Default is False.
    """
    # Start of the analysis 
    color_msg(f"Inpecting event {event_number} from DTNTuples", "green")

    # Create the Ntuple object
    _ntuple_module, _ntuple_class = RUN_CONFIG.ntuple_source.rsplit(".", 1)
    _ntuple_module = importlib.import_module(_ntuple_module)
    _NTUPLE =  getattr(_ntuple_module, _ntuple_class)

    ntuple = _NTUPLE(
        inputFolder=inpath,
        maxfiles=maxfiles,
    )

        # setting up which histograms will be fill
    if isinstance(event_number, str):
        event_indices = eval(f"slice({event_number.replace(':', ',')})")
        events = ntuple.events[event_indices]
        beg, *end = event_number.split(":")
        try:
            total = (int(end[0]) - int(beg)) // int(end[1])
        except IndexError:
            total = int(end[0]) - int(beg)
        print(f"Total events: {total}")
    else:
        events = [ntuple.events[event_number]]
        total = 1
    from time import sleep
    for ev in tqdm(
        events,
        total=total,
        desc=color_msg(f"Running:", color="purple", indentLevel=1, return_str=True),
        ncols=100,
        ascii=True,
        unit="event"
    ):
        if not ev:
            tqdm.write(color_msg(f"Event not pass filter: {ev}", color="red", return_str=True))

        tqdm.write(ev.__str__(indentLevel=1))
        sleep(1)

    color_msg(f"Done!", color="green")
