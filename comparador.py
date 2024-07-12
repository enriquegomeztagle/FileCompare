import streamlit as st
import pandas as pd

# Función para leer el archivo y actualizar la barra de progreso
def load_data_with_progress(uploaded_file, delimiter, encoding):
    if uploaded_file is not None:
        if uploaded_file.name.endswith(('.csv', '.txt')):
            try:
                with st.spinner('Cargando archivo...'):
                    file_size = uploaded_file.size
                    
                    progress_bar = st.progress(0)
                    df = pd.DataFrame()
                    
                    # Leer el archivo en partes y actualizar la barra de progreso
                    for i, chunk in enumerate(pd.read_csv(uploaded_file, delimiter=delimiter, encoding=encoding, chunksize=1000)):
                        df = pd.concat([df, chunk])
                        progress = min((i + 1) * chunk.memory_usage(deep=True).sum() / file_size, 1.0)
                        progress_bar.progress(progress)
                    
                    return df
            except Exception as e:
                st.error(f"Error al procesar el archivo: {e}")
        else:
            st.error("Formato de archivo no soportado. Por favor, carga un archivo CSV o TXT.")
    return None

# Función para comparar los dataframes
def compare_dataframes(df1, df2):
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Primer DataFrame")
        st.write(f"Longitud del DataFrame: {len(df1)}")
        st.write("Columnas:", df1.columns.tolist())
    
    with col2:
        st.write("### Segundo DataFrame")
        st.write(f"Longitud del DataFrame: {len(df2)}")
        st.write("Columnas:", df2.columns.tolist())

    if df1.equals(df2):
        st.success("Los archivos son idénticos!")
    else:
        st.warning("Los archivos tienen diferencias.")

# Función principal de la aplicación
def main():
    st.title('Comparador de Archivos')
    
    col1, col2 = st.columns(2)
    
    with col1:
        file1 = st.file_uploader("Carga el primer archivo", type=['csv', 'txt'], key='file1')
        delimiter1 = st.selectbox("Selecciona el delimitador para el primer archivo", 
                                  options=[',', '|', ';', '\t'], index=0, key='delim1')
        encoding1 = st.selectbox("Selecciona la codificación para el primer archivo",
                                 options=['utf-8', 'latin-1'], index=0, key='enc1')
        
        # Previsualización del primer archivo
        if file1 is not None:
            df1_preview = load_data_with_progress(file1, delimiter1, encoding1)
            if df1_preview is not None:
                st.write("### Previsualización del primer archivo")
                st.dataframe(df1_preview.head())

    with col2:
        file2 = st.file_uploader("Carga el segundo archivo", type=['csv', 'txt'], key='file2')
        delimiter2 = st.selectbox("Selecciona el delimitador para el segundo archivo", 
                                  options=[',', '|', ';', '\t'], index=0, key='delim2')
        encoding2 = st.selectbox("Selecciona la codificación para el segundo archivo",
                                 options=['utf-8', 'latin-1'], index=0, key='enc2')
        
        # Previsualización del segundo archivo
        if file2 is not None:
            df2_preview = load_data_with_progress(file2, delimiter2, encoding2)
            if df2_preview is not None:
                st.write("### Previsualización del segundo archivo")
                st.dataframe(df2_preview.head())
    
    if st.button("Comparar archivos"):
        if file1 is not None and file2 is not None:
            df1 = load_data_with_progress(file1, delimiter1, encoding1)
            df2 = load_data_with_progress(file2, delimiter2, encoding2)
            
            if df1 is not None and df2 is not None:
                compare_dataframes(df1, df2)
        else:
            st.error("Por favor, carga ambos archivos para proceder con la comparación.")

if __name__ == "__main__":
    main()
