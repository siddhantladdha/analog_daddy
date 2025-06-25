import streamlit as st

st.title("Demo: Custom Tables with Borders (Markdown Only)")

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
