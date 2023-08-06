from os import PathLike, mkdir, path
from pathlib import Path
from typing import Union, Optional

import pandas as pd
from pandas.tseries.offsets import MonthEnd

from econuy.utils import updates, metadata
from econuy.utils.lstrings import cpi_url


def get(update_path: Union[str, PathLike, None] = None,
        revise_rows: Union[str, int] = "nodup",
        save_path: Union[str, PathLike, None] = None,
        force_update: bool = False,
        name: Optional[str] = None) -> pd.DataFrame:
    """Get CPI data.

    Parameters
    ----------
    update_path : str, os.PathLike or None, default None
        Path or path-like string pointing to a directory where to find a CSV
        for updating, or ``None``, don't update.
    revise_rows : {'nodup', 'auto', int}
        Defines how to process data updates. An integer indicates how many rows
        to remove from the tail of the dataframe and replace with new data.
        String can either be ``auto``, which automatically determines number of
        rows to replace from the inferred data frequency, or ``nodup``,
        which replaces existing periods with new data.
    save_path : str, os.PathLike or None, default None
        Path or path-like string pointing to a directory where to save the CSV,
        or ``None``, don't save.
    force_update : bool, default False
        If ``True``, fetch data and update existing data even if it was
        modified within its update window (for consumer prices, 25 days).
    name : str, default None
        CSV filename for updating and/or saving.

    Returns
    -------
    Monthly CPI index : pd.DataFrame

    """
    update_threshold = 25
    if name is None:
        name = "cpi"

    if update_path is not None:
        full_update_path = (Path(update_path) / name).with_suffix(".csv")
        delta, previous_data = updates._check_modified(full_update_path)

        if delta < update_threshold and force_update is False:
            print(f"{full_update_path} was modified within "
                  f"{update_threshold} day(s). Skipping download...")
            return previous_data

    cpi_raw = pd.read_excel(cpi_url, skiprows=7).dropna(axis=0, thresh=2)
    cpi = (cpi_raw.drop(["Mensual", "Acum.año", "Acum.12 meses"], axis=1).
           dropna(axis=0, how="all").set_index("Mes y año").rename_axis(None))
    cpi.columns = ["Índice de precios al consumo"]
    cpi.index = cpi.index + MonthEnd(1)

    if update_path is not None:
        cpi = updates._revise(new_data=cpi, prev_data=previous_data,
                              revise_rows=revise_rows)

    cpi = cpi.apply(pd.to_numeric, errors="coerce")
    metadata._set(cpi, area="Precios y salarios", currency="-",
                  inf_adj="No", unit="2010-10-31=100", seas_adj="NSA",
                  ts_type="-", cumperiods=1)

    if save_path is not None:
        full_save_path = (Path(save_path) / name).with_suffix(".csv")
        if not path.exists(path.dirname(full_save_path)):
            mkdir(path.dirname(full_save_path))
        cpi.to_csv(full_save_path)

    return cpi
