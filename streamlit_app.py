import streamlit as st

st.title("Ejemplo con Streamlit")
x = st.slider("Selecciona un valor", 0, 100, 50)
st.write("Has seleccionado:", x)
