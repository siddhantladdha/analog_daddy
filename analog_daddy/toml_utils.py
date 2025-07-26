import os
import logging
from typing import List, Dict, Any
import pandas as pd
import tomlkit

def circuit_toml_reader(lut_metadata: List = None, filepath: str = None) -> Dict[str, Any]:
    """
    Read the circuit configuration from a TOML file using tomlkit.
    If no filepath is provided, use a default path.
    Performs the following checks
    1. if the file exists and is readable.
    2. if the file has all the necessary sections and keys.
    3. if the technology_info is present and matches the lut_metadata loaded.
    4. if the device types in the lut_metadata match the device types in the TOML file.

    """
    # TODO:change the following eventually reading analog_daddy config file
    # to avoid magic strings.
    REQUIRED_KEYS = {"type", "length", "gm_id", "id", "w"}
    # If no filepath is provided, use a default path of demo_circuit.toml
    if filepath is None:
        filepath = os.path.join(
                            os.path.dirname(__file__),
                            "..", "..", ".config", "demo_circuit.toml"
                            )
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            # toml file is now loaded as a TOMLDocument (preserves comments)
            toml_doc = tomlkit.load(f)
            # Convert to dict for downstream compatibility
            toml_dict = dict(toml_doc)
    except FileNotFoundError as e:
        msg = f"The TOML file is not found: {filepath}"
        logging.error(msg)
        raise FileNotFoundError(msg) from e
    # if st.session_state.get("debug_mode_selector"):
    #     with st.expander("TOML Debug Info", expanded=True):
    #         st.write(toml_dict)
    # Perform checks on the loaded TOML file
    if toml_dict.get("metadata", {}).get("technology_info", {}) != lut_metadata["Info"]:
        msg = """The technology_info in the TOML file does not match the LUT info.
            Either (A) Upload the correct LUT file or (B) If porting to a different technology,
            ensure the technology_info and the device types in TOML
            matches the target technology's Info and device types."""
        logging.error(msg)
        raise ValueError(msg)
    # Convert the circuit part to DataFrame
    circuit_dict = {k: v for k, v in toml_dict.items() if k != "metadata"}
    # iterate over each device type in the LUT metadata
    for device_name, device_data in circuit_dict.items():
        missing = REQUIRED_KEYS - device_data.keys()
        if missing:
            msg = (
                f"The device: {device_name} in the TOML file is "
                f"missing key(s): {missing}. "
                "Please ensure all required keys are present in the TOML file."
            )
            logging.error(msg)
            raise ValueError(msg)

        # Proceed if all required keys are present
        # Check available device types.
        if device_data["type"] not in lut_metadata["Device Type"]:
            msg = (
                f"Device type: {device_data['type']} for {device_name} in the TOML file "
                f"does not match the available devices {lut_metadata['Device Type']} "
                f"in LUT uploaded. If porting please ensure initialising with any "
                f"available device type."
            )
            logging.error(msg)
            raise ValueError(msg)
    circuit_df = pd.DataFrame.from_dict(
                    circuit_dict, orient="index"
                    ).reset_index().rename(
                        columns={"index": "transistor_name"}
                )
    return circuit_df
