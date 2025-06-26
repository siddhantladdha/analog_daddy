from collections import defaultdict
import textwrap
import streamlit as st
import numpy as np
from analog_daddy.look_up import look_up
from parse_si import format_si_or_scientific as fmt_str_si

st.title("Analog Daddy Dashboard")

# region File Uploading Logic

# Drag and drop file uploader for up to two numpy files only, with session persistence
st.markdown("#### Drag and Drop up to Two NumPy (.npy) Files Below:")

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'lut_roots' not in st.session_state:
    st.session_state.lut_roots = []

uploaded_files = st.file_uploader(
    "Choose up to 2 .npy files", type=["npy"], accept_multiple_files=True, key="npy_uploader"
)

# Update session state only if new files are uploaded
if uploaded_files:
    if len(uploaded_files) > 2:
        st.error("Please upload no more than two .npy files.")
    else:
        st.session_state.uploaded_files = uploaded_files
        st.session_state.lut_roots = []
        for file in uploaded_files:
            st.success(f"Uploaded file: {file.name}")
            try:
                lut_root = np.load(file, allow_pickle=True).item()
                st.session_state.lut_roots.append(lut_root)
            except EOFError as e:
                st.error(f"Failed to load {file.name}: {e}. "
                         "The session has been refreshed. Please re-upload the files.")
            except ValueError as e:
                st.error(f"Failed to load {file.name}: {e}")
            except Exception as e:
                st.error(f"Failed to load {file.name}: {e}")
            del file
elif st.session_state.uploaded_files:
    st.session_state.lut_roots = []
    for file in st.session_state.uploaded_files:
        st.info(f"(Session) File: {file.name}")
        try:
            lut_root = np.load(file, allow_pickle=True).item()
            st.session_state.lut_roots.append(lut_root)
        except EOFError as e:
            st.error(f"Failed to load {file.name}: {e}. "
                    "The session has been refreshed. Please re-upload the files.")
        except ValueError as e:
            st.error(f"Failed to load {file.name}: {e}")
        except Exception as e:
            st.error(f"Failed to load {file.name}: {e}")
        del file
# endregion File Uploading Logic

lut_roots = st.session_state.lut_roots

# region LUT Metadata Table
headers = ["Device Type", "Temperature/Corner", "Info"]
# Only process device_metadata if both lists are not empty
if st.session_state.lut_roots:
    device_types = [
        [k for k, v in lut.items() if isinstance(v, dict)]
        for lut in lut_roots
    ]

    lut_metadata = [
        {
            "Device Type":          device_types[i],
            "Temperature/Corner":   f"{st.session_state.lut_roots[i].get('temperature')}°C : "
                                    f"{st.session_state.lut_roots[i].get('corner')}",
            "Info":                 st.session_state.lut_roots[i].get('info')
        }
        for i in range(len(st.session_state.lut_roots))
    ]
else:
    st.error("No LUT metadata available. Please upload valid .npy files.")
    st.stop()

st.markdown("## LUT Metadata Table")

# lut_metadata is a list of dicts, one per row

# Prepare table: first row is headers, then the data rows
table = [headers] + [
    [lut_metadata_entry["Device Type"],
     lut_metadata_entry["Temperature/Corner"],
     lut_metadata_entry["Info"]]
    for lut_metadata_entry in lut_metadata
]

column_widths = [1, 1, 1]  # Adjust widths for each column
for row_idx, row_value in enumerate(table):
    columns = st.columns(column_widths, border=True, gap="small")
    for col_idx, (column, cell) in enumerate(zip(columns, row_value)):
        if row_idx == 0: # Header row
            column.markdown(f"**{cell}**")
        else: # Data rows
            if col_idx == 0:  # Device Type column
                selected = column.selectbox(
                    label="Lable_text",
                    options=lut_metadata[row_idx - 1]["Device Type"],
                    key=f"selected_device_type_{row_idx - 1}",
                    label_visibility="collapsed"
                )
            else:
                column.write(cell)
# endregion

# region Variable Selection and Display
st.markdown("## Variable Selection and Display")

parameters_list = []

for i, lut in enumerate(lut_roots):
    selected_device_type = st.session_state.get(f"selected_device_type_{i}")
    if not selected_device_type:
        continue
    device_lut = lut.get(selected_device_type, {})
    dependent_vars = []
    independent_vars = []
    for key, value in device_lut.items():
        if isinstance(value, np.ndarray):
            if value.ndim == 4:
                dependent_vars.append(key)
            elif value.ndim == 1 and value.size > 1:
                independent_vars.append((key, value))
    parameters_list.append({
        "selected_device_type": selected_device_type,
        "dependent_vars": dependent_vars,
        "independent_vars": [k for k, _ in independent_vars]
    })

if len(parameters_list) == 2: # Only compare if two LUTs are selected
    if set(parameters_list[0]["dependent_vars"]) != set(parameters_list[1]["dependent_vars"]):
        st.error("Dependent variables does not match between two LUT's")
        st.stop()
    if set(parameters_list[0]["independent_vars"]) != set(parameters_list[1]["independent_vars"]):
        st.error("Independent variables does not match between two LUT's")
        st.stop()
# Adding important design variables to the independent_vars list
design_vars = ["gm/id", "id/w"]
for param in parameters_list:
    param["independent_vars"].extend(design_vars)
# Adding ratios to the dependent_vars list
ratio_vars = []
for i, var1 in enumerate(parameters_list[0]["dependent_vars"]):
    for j, var2 in enumerate(parameters_list[0]["dependent_vars"]):
        if i != j:
            ratio_vars.append(f"{var1}/{var2}")
    ratio_vars.append(f"{var1}/w")
dependent_var_options = parameters_list[0]["dependent_vars"] + ratio_vars


# --- Mutually Exclusive Selection for Independent Vars using st.multiselect ---
if not parameters_list : # Check if parameters_list is empty
    st.error("No parameters available. Please select a device type first.")
    st.stop()
if len(independent_vars) <= 1:
    st.error("Independent variables dimensions not correct. Check LUT format.")
    st.stop()

selected_independent_var = st.multiselect(
    textwrap.dedent("""\
                    **Independent variables**\n
                    Choose upto two variables.\n
                    The **first** option is used as the **x-axis**.\n
                    The **second** option is used for the **parametric axis**."""),
    parameters_list[0]["independent_vars"],
    default=None,
    max_selections=2
)
selected_dependent_var = st.selectbox("**Dependent variable**", dependent_var_options, index=None)

if selected_dependent_var and selected_independent_var:
    if selected_dependent_var in selected_independent_var:
        st.error("Dependent variable cannot be an independent variable. Please select a different variable.")
        st.stop()

st.write(f"""- Independent variable: {selected_independent_var}\n
- Dependent Variable: {selected_dependent_var}""")

# endregion
# Build nested min/max dict for independent variables and gm/id arrays
independent_var_minmax = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

for lut_number, lut in enumerate(lut_roots):
    for device in lut_metadata[lut_number]["Device Type"]:
        device_data_dict = lut.get(device, {})
        for key, value in device_data_dict.items():
            if isinstance(value, np.ndarray):
                if (value.ndim == 1 and value.size > 1):
                    independent_var_minmax[lut_number][device][key]["min"] = float(np.min(value))
                    independent_var_minmax[lut_number][device][key]["max"] = float(np.max(value))
                    independent_var_minmax[lut_number][device][key]["step"] = float(value[1] - value[0])
                elif (value.ndim == 4 and key in ['gm', 'id']):
                    if key == 'gm':
                        independent_var_minmax[lut_number][device]["gm/id"]["min"] = None
                        independent_var_minmax[lut_number][device]["gm/id"]["max"] = None
                        independent_var_minmax[lut_number][device]["gm/id"]["step"] = None
                    elif key == 'id':
                        independent_var_minmax[lut_number][device]["id/w"]["min"] = None
                        independent_var_minmax[lut_number][device]["id/w"]["max"] = None
                        independent_var_minmax[lut_number][device]["id/w"]["step"] = None


independent_var_minmax = {
                            k: {
                                dk: dict(dv)
                                for dk, dv in v.items()
                                }
                            for k, v in independent_var_minmax.items()
                        }

for lut_number, lut in enumerate(lut_roots):
    for device in lut_metadata[lut_number]["Device Type"]:
        device_data_dict = lut.get(device, {})
        # Add min/max for gm/id and id/w using look_up function
        gm_id = look_up(
            device_data_dict,
            'gm_id',
            length=float(np.min(device_data_dict["length"])),
            gs=np.arange(
                independent_var_minmax[lut_number][device]["gs"]["min"],
                independent_var_minmax[lut_number][device]["gs"]["max"],
                independent_var_minmax[lut_number][device]["gs"]["step"]
                ),
            ds=independent_var_minmax[lut_number][device]["ds"]["max"],
            sb=independent_var_minmax[lut_number][device]["sb"]["min"]
            )
        id_w = look_up(
            device_data_dict,
            'id_w',
            length=float(np.min(device_data_dict["length"])),
            gs=np.arange(
                independent_var_minmax[lut_number][device]["gs"]["min"],
                independent_var_minmax[lut_number][device]["gs"]["max"],
                independent_var_minmax[lut_number][device]["gs"]["step"]
                ),
            ds=independent_var_minmax[lut_number][device]["ds"]["max"],
            sb=independent_var_minmax[lut_number][device]["sb"]["min"]
            )
        independent_var_minmax[lut_number][device]["gm/id"]["max"] = float(np.max(gm_id))
        independent_var_minmax[lut_number][device]["gm/id"]["min"] = float(np.min(gm_id))
        independent_var_minmax[lut_number][device]["gm/id"]["step"] = 0.5
        independent_var_minmax[lut_number][device]["id/w"]["max"] = float(np.max(id_w))
        independent_var_minmax[lut_number][device]["id/w"]["min"] = float(np.min(id_w))
        # Logarithmic step size for id/w
        id_w_logspace = np.logspace(np.log10(
            independent_var_minmax[lut_number][device]["id/w"]["min"]),
            independent_var_minmax[lut_number][device]["id/w"]["max"],
            100
            )
        # Multiplicative step size
        independent_var_minmax[lut_number][device]["id/w"]["step"] = (
            id_w_logspace[1] / id_w_logspace[0]
        )

var_default = { }
# create input fields for start:step:stop.
# Assume 'selected' is your list of selected independent variables from st.multiselect
if selected_independent_var:
    for var in selected_independent_var:

        # check if the independent variables min/max are the same for both LUTs
        if len(parameters_list) == 2:
            for elem in ["min", "max"]:
                if independent_var_minmax[0][st.session_state.get("selected_device_type_0")][var][elem] != independent_var_minmax[1][st.session_state.get("selected_device_type_1")][var][elem]:
                    st.warning(f"Independent variable {var} {elem} value does not match between two LUTs for given device type. Smaller of the two will be used.")
                    var_default[elem] = min(
                        abs(independent_var_minmax[0][st.session_state.get("selected_device_type_0")][var][elem]),
                        abs(independent_var_minmax[1][st.session_state.get("selected_device_type_1")][var][elem])
                    )
                else:
                    var_default[elem] = independent_var_minmax[0][st.session_state.get("selected_device_type_0")][var][elem]
        else:
            # If only one LUT is selected, use its values directly
            var_default["min"] = independent_var_minmax[0][st.session_state.get("selected_device_type_0")][var]["min"]
            var_default["max"] = independent_var_minmax[0][st.session_state.get("selected_device_type_0")][var]["max"]

        st.markdown(f"**Range for {var}:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            start = st.text_input(f"{var} start", key=f"{var}_start", value=fmt_str_si(var_default["min"]))
        with col2:
            stop = st.text_input(f"{var} stop", key=f"{var}_stop", value=fmt_str_si(var_default["max"]))
        with col3:
            # we don't bother comparing step size between two LUTs, just use the first one
            step = st.text_input(f"{var} step", key=f"{var}_step", value=fmt_str_si(independent_var_minmax[0][st.session_state.get("selected_device_type_0")][var]["step"]))
