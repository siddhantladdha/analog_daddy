import streamlit as st
import numpy as np
import pandas as pd

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

parameters_list