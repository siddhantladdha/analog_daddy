import streamlit as st
import numpy as np

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

# Table 1: 4x4 (excluding header)
table1 = """
| Col 1 | Col 2 | Col 3 | Col 4 |
|-------|-------|-------|-------|
|  A1   |  B1   |  C1   |  D1   |
|  A2   |  B2   |  C2   |  D2   |
|  A3   |  B3   |  C3   |  D3   |
|  A4   |  B4   |  C4   |  D4   |
"""

# Table 2: 3x4 (excluding header)
table2 = """
| Col A | Col B | Col C | Col D |
|-------|-------|-------|-------|
|  X1   |  Y1   |  Z1   |  W1   |
|  X2   |  Y2   |  Z2   |  W2   |
|  X3   |  Y3   |  Z3   |  W3   |
"""

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Table 1: 4x4")
    st.markdown(table1)

with col2:
    st.markdown("### Table 2: 3x4")
    st.markdown(table2)
