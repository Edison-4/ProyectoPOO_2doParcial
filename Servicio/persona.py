# Integrante:
# -- Chinga Michelle
# -- Ortiz Michael
# -- Plaza Edison
# -- Villao Carla

from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QMainWindow, QMessageBox

# Asegúrate de que estos import coincidan con tus archivos
from GUI.Datos.personaDAO import PersonaDAO
from GUI.Dominio.persona import Persona
from GUI.UI.vtnPrincipal import Ui_vtnPrincipal


class PersonaServicio(QMainWindow):
    '''
    Clase que genera la logica de los objetos persona (Controlador)
    '''

    def __init__(self):
        super(PersonaServicio, self).__init__()
        self.ui = Ui_vtnPrincipal()
        self.ui.setupUi(self)

        # --- CONEXIÓN DE BOTONES ---
        # Botones del GroupBox (CRUD)
        self.ui.btninsertar.clicked.connect(self.guardar)
        self.ui.btnbuscar.clicked.connect(self.buscar)
        self.ui.btnactualizar.clicked.connect(self.actualizar)
        self.ui.btneliminar.clicked.connect(self.eliminar)

        # Botones inferiores
        self.ui.btnGuardar.clicked.connect(self.guardar)
        self.ui.btnlimpiar.clicked.connect(self.limpiar)

        # Validadores
        self.ui.txtcedula.setValidator(QIntValidator())  # Solo números en la cédula
        self.ui.txtcostservicio.setValidator(QIntValidator())

    def obtener_datos_ui(self):
        """Método auxiliar para leer todos los campos y crear el objeto Persona"""
        return Persona(
            cedula=self.ui.txtcedula.text(),
            nombre=self.ui.txtNombre.text(),
            apellido=self.ui.txtApellido.text(),
            ruta=self.ui.cbruta.currentText(),
            costo=self.ui.txtcostservicio.text(),
            tipo_servicio=self.ui.cbtiposervicio.currentText()
        )

    def guardar(self):
        # 1. Recolección de datos directos de la interfaz
        cedula = self.ui.txtcedula.text()
        nombre = self.ui.txtNombre.text()
        apellido = self.ui.txtApellido.text()
        ruta = self.ui.cbruta.currentText()
        costo = self.ui.txtcostservicio.text()
        tipo = self.ui.cbtiposervicio.currentText()

        # 2. Validaciones (El orden importa: si falla uno, se detiene y avisa)

        # --- VALIDACIÓN CÉDULA (Prioridad) ---
        if cedula == "" or len(cedula) < 10:
            QMessageBox.warning(self, 'Advertencia', 'Debe ingresar una cédula válida (10 dígitos).')
            return

        # --- VALIDACIONES DE CAMPOS VACÍOS ---
        elif nombre == "":
            QMessageBox.warning(self, 'Advertencia', 'Debe ingresar el nombre.')
            return

        elif apellido == "":
            QMessageBox.warning(self, 'Advertencia', 'Debe ingresar el apellido.')
            return

        elif ruta == "Seleccionar" or ruta == "":
            QMessageBox.warning(self, 'Advertencia', 'Debe seleccionar una ruta.')
            return

        # --- AQUÍ ESTÁ LA VALIDACIÓN DEL COSTO ---
        elif costo == "":
            QMessageBox.warning(self, 'Advertencia', 'Debe ingresar el costo del servicio.')
            return

        elif tipo == "Seleccionar":
            QMessageBox.warning(self, 'Advertencia', 'Debe seleccionar un tipo de servicio.')
            return

        # 3. Si pasa todas las validaciones, creamos el objeto y guardamos
        else:
            # Usamos los datos que ya capturamos arriba
            persona = Persona(
                cedula=cedula,
                nombre=nombre,
                apellido=apellido,
                ruta=ruta,
                costo=costo,
                tipo_servicio=tipo
            )

            respuesta_dict = PersonaDAO.insertar_persona(persona)

            if respuesta_dict['ejecuto']:
                self.ui.statusbar.showMessage('Se guardó la información correctamente', 3000)
                self.limpiar()
            else:
                QMessageBox.critical(self, 'Error', respuesta_dict['mensaje'])

    def buscar(self):
        # Usamos el campo de cédula principal para buscar
        cedula = self.ui.txtcedula.text()

        if len(cedula) < 3:  # Validación mínima
            QMessageBox.warning(self, 'Advertencia', 'Ingrese la cédula en el campo correspondiente para buscar.')
            return

        persona = PersonaDAO.seleccionar_persona(cedula)

        if persona:
            # Rellenar los campos con los datos encontrados
            self.ui.txtNombre.setText(persona.nombre)
            self.ui.txtApellido.setText(persona.apellido)
            self.ui.cbruta.setCurrentText(persona.ruta)
            self.ui.txtcostservicio.setText(str(persona.costo))
            self.ui.cbtiposervicio.setCurrentText(persona.tipo_servicio)

            self.ui.statusbar.showMessage('Registro encontrado', 2000)
        else:
            QMessageBox.warning(self, 'Advertencia', 'No existe registro con esa cédula.')
            # Opcional: Limpiar si no encuentra nada, para evitar confusiones
            # self.limpiar()

    def actualizar(self):
        persona = self.obtener_datos_ui()

        if not persona.cedula:
            QMessageBox.warning(self, 'Advertencia', 'Se requiere la cédula para actualizar.')
            return

        # --- LLAMADA AL DAO (ACTUALIZAR) ---
        respuesta_dict = PersonaDAO.actualizar_persona(persona)

        if respuesta_dict['ejecuto']:
            self.ui.statusbar.showMessage(respuesta_dict['mensaje'], 3000)
            self.limpiar()
        else:
            QMessageBox.critical(self, 'Error', respuesta_dict['mensaje'])

    def eliminar(self):
        cedula = self.ui.txtcedula.text()

        if not cedula:
            QMessageBox.warning(self, 'Advertencia', 'Ingrese la cédula para eliminar.')
            return

        confirmacion = QMessageBox.question(self, 'Confirmar',
                                            f'¿Está seguro de eliminar el registro {cedula}?',
                                            QMessageBox.Yes | QMessageBox.No)

        if confirmacion == QMessageBox.Yes:
            # --- LLAMADA AL DAO (ELIMINAR) ---
            respuesta_dict = PersonaDAO.eliminar_persona(cedula)

            if respuesta_dict['ejecuto']:
                self.ui.statusbar.showMessage(respuesta_dict['mensaje'], 3000)
                self.limpiar()
            else:
                QMessageBox.critical(self, 'Error', respuesta_dict['mensaje'])

    def limpiar(self):
        self.ui.txtNombre.clear()
        self.ui.txtApellido.clear()
        self.ui.txtcedula.clear()
        self.ui.cbruta.setCurrentIndex(0)
        self.ui.txtcostservicio.clear()
        self.ui.cbtiposervicio.setCurrentIndex(0)  # Vuelve al primer ítem ("Seleccionar")
        self.ui.statusbar.showMessage('Campos limpiados', 2000)