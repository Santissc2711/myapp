
import streamlit as st
import pandas as pd
import sklearn
from sklearn.preprocessing import MinMaxScaler

dataset = pd.read_csv('https://raw.githubusercontent.com/Santissc2711/myapp/main/data_football_ratings.csv',sep=",")
dataset = dataset[~((dataset['rater'] == 'Kicker') | (dataset['rater'] == 'SofaScore')| (dataset['rater'] == 'Bild') | 
              (dataset['rater'] == 'SkySports') | (dataset['rater'] == 'TheGuardian'))]
data= dataset[~((dataset['pos'] == 'GK'))]
data= dataset[~((dataset['pos'] == 'Sub'))]

#arreglado
# Función para guardar resultados en un archivo
def guardar_resultados(opcion_seleccionada, nombre_jugador, df, prediccion):
    # Crear un diccionario con la información
    resultados = {
        'Jugador': nombre_jugador,
        'Opción Seleccionada': opcion_seleccionada,
        'Estadísticas': df.to_dict(orient='records')[0],
        'Predicción': prediccion.tolist()[0]
    }

    # Guardar el diccionario en un archivo
    with open('resultados.pkl', 'ab') as file:
        pickle.dump(resultados, file)

# Función para borrar los resultados guardados
def borrar_resultados():
    # Borrar el contenido del archivo
    open('resultados.pkl', 'w').close()
    st.success('Resultados borrados exitosamente.')

# Función para cargar resultados guardados
def cargar_resultados():
    try:
        # Cargar resultados del archivo
        with open('resultados.pkl', 'rb') as file:
            resultados = []
            while True:
                try:
                    resultado = pickle.load(file)
                    resultados.append(resultado)
                except EOFError:
                    break
        return resultados
    except FileNotFoundError:
        return []

st.title("Analisis predictivo de jugadores de futbol por estadisticas")
nombre_jugador = st.sidebar.text_input("Ingrese el nombre del jugador:")

#barra lateral

modo_seleccionado = st.sidebar.selectbox("Seleccione el modo", ["Individual", "Grupal"])


# barra desplegable
opcion_seleccionada = st.sidebar.selectbox("Seleccione variable",["Incidencia en la victoria", "Puntaje general"])

# Almacenar los datos ingresados por el usuario
datos_ingresados = []




# Mostrar contenido basado en la opción seleccionada
if modo_seleccionado == "Individual":
    if opcion_seleccionada == "Incidencia en la victoria":
        st.header("Prediccion en la incidencia de victoria, 0 tiene incidencia y 1 no tiene incidencia")
        st.markdown("Rellene todos los recuadros tomando en cuenta las estadisticas del futbolista")
        
        
        # Crear 6 cuadros para ingresar números reales
        titulos_cuadros = ["original_rating", "goals", "assists", "shots_ontarget", "countattack", "flow_success"]
        for i, titulo in enumerate(titulos_cuadros):
            # Obtener el número ingresado por el usuario
            numero = st.number_input(f"{titulo}:", value=0.0, step=0.1)
            datos_ingresados.append(numero)
            

        # Crear un DataFrame con los datos ingresados
        df = pd.DataFrame(data=[datos_ingresados], columns=titulos_cuadros)
        st.header("Estadisticas del jugador:")
        st.write(df)

        # Realizar el escalamiento de los datos
        min_max_scaler = MinMaxScaler()
        min_max_scaler.fit(dataset[['original_rating', 'goals','assists','shots_ontarget','countattack','flow_success']]) #Ajuste de los parametros: max - min


        #cargar el mejor modelo
    
        # open a file, where you stored the pickled data

        nombreArchivo = 'Modelo_lost.pkl'
        modeloCargado = pickle.load(open(nombreArchivo, 'rb'))
        
      
      
        #Predicccion con el dataframe creado
        prediccion = modelo_cargado.predict(min_max_scaler.transform(df))
        
        # Mostrar la predicción
        st.header("Predicción del modelo para el jugador **{}**:".format(nombre_jugador))
        st.markdown(prediccion)



    elif opcion_seleccionada == "Puntaje general":
        st.header("Prediccion en el puntage general")
        st.markdown("Rellene todos los recuadros tomando en cuenta las estadisticas del futbolista.")

        # Crear cuadros para ingresar números reales
        titulos_cuadros = ['goals','assists','shots_ontarget','chances2score','drib_success','keypasses','touches',
                    'crosses_acc','grduels_w','aerials_w','wasfouled','tackles','tballs_acc',
                    'rcards','countattack','flow_centrality','flow_success','betweenness2goals','lost']
        for i, titulo in enumerate(titulos_cuadros):
            # Obtener el número ingresado por el usuario
            numero = st.number_input(f"{titulo}:", value=0.0, step=0.1)
            datos_ingresados.append(numero)
            

        # Crear un DataFrame con los datos ingresados
        df = pd.DataFrame(data=[datos_ingresados], columns=titulos_cuadros)
        st.header("Estadisticas del jugador:")
        st.write(df)

        # Realizar el escalamiento de los datos
        min_max_scaler = MinMaxScaler()
        min_max_scaler.fit(dataset[['goals','assists','shots_ontarget','chances2score','drib_success','keypasses','touches',
                    'crosses_acc','grduels_w','aerials_w','wasfouled','tackles','tballs_acc',
                    'rcards','countattack','flow_centrality','flow_success','betweenness2goals','lost']]) #Ajuste de los parametros: max - min


        #cargar el mejor modelo
        # open a file, where you stored the pickled data
        nombreArchivo = 'Modelo_rating.pkl'
        modeloCargado = pickle.load(open(nombreArchivo, 'rb'))

        #Predicccion con el dataframe creado
        prediccion = modelo_cargado.predict(min_max_scaler.transform(df))
        
        # Mostrar la predicción
        st.header("".format(nombre_jugador))
        st.markdown(prediccion)



# Variables grupales
elif modo_seleccionado == "Grupal":
    uploaded_file = st.file_uploader("Cargar archivo CSV o Excel para análisis grupal", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')  # Intenta con UTF-8 primero
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding='latin-1')

        # Realizar el escalamiento de los datos
        min_max_scaler = MinMaxScaler()

        # Seleccionar el modelo adecuado según la opción
        if opcion_seleccionada == "Incidencia en la victoria":
            st.header("Prediccion en la incidencia de victoria, 0 tiene incidencia y 1 no tiene incidencia")
            # Seleccionar el modelo
            nombreArchivo = 'Modelo_lost.pkl'
          modeloCargado = pickle.load(open(nombreArchivo, 'rb'))
            min_max_scaler.fit(dataset[['original_rating', 'goals', 'assists', 'shots_ontarget', 'countattack', 'flow_success']])
            prediccion = modelo_cargado.predict(min_max_scaler.transform(df))
             # Mostrar la predicción
            st.markdown("Predicción del modelo en orden para los jugadores añadidos")
            st.write(prediccion)

        else:
            st.header("Prediccion en el puntage general")
            nombreArchivo = 'Modelo_rating.pkl'
            modeloCargado = pickle.load(open(nombreArchivo, 'rb'))
            min_max_scaler.fit(dataset[['goals','assists','shots_ontarget','chances2score','drib_success','keypasses','touches',
                                    'crosses_acc','grduels_w','aerials_w','wasfouled','tackles','tballs_acc',
                                    'rcards','countattack','flow_centrality','flow_success','betweenness2goals','lost']])
            prediccion = modelo_cargado.predict(min_max_scaler.transform(df))
             # Mostrar la predicción
            st.write("".format(nombre_jugador))
            st.markdown("Predicción del modelo en orden para los jugadores añadidos")
            st.write(prediccion)



# Crear dos columnas en la barra lateral
col1, col2 = st.sidebar.columns(2)

# Crear botones en las columnas
if col1.button('Guardar Resultados'):
    guardar_resultados(opcion_seleccionada, nombre_jugador, df, prediccion)

if col2.button('Borrar Resultados'):
    borrar_resultados()

    # Sección para mostrar resultados almacenados
st.header("Resultados Almacenados")
resultados_almacenados = cargar_resultados()
for resultado in resultados_almacenados:
    st.markdown(f"**Jugador:** {resultado['Jugador']}")
    st.markdown(f"**Opción Seleccionada:** {resultado['Opción Seleccionada']}")
    st.markdown(f"**Estadísticas:** {resultado['Estadísticas']}")
    st.markdown(f"**Predicción:** {resultado['Predicción']}")
    st.markdown("---")
