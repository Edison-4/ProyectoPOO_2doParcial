import valor

class Persona:
    '''
    Clase que permite crear objetos con los datos del servicio de transporte
    '''
    def __init__(self, cedula:str=None, nombre:str=None, apellido:str=None,
                 ruta:str=None, costo:str=None, tipo_servicio:str=None):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.ruta = ruta
        self.costo = costo
        self.tipo_servicio = tipo_servicio

    # --- CEDULA ---
    @property
    def cedula(self):
        return self._cedula

    @cedula.setter
    def cedula(self, valor):
        # Si está vacío, lo guardamos como texto vacío sin dar error
        if valor is None:
            self._cedula = ""
        else:
            self._cedula = valor
        # NOTA: Quitamos el 'raise ValueError' para evitar el crash.
        # La validación la haremos en la ventana (Servicio).

    # --- NOMBRE ---
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor if valor else ""

    # --- APELLIDO ---
    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, valor):
        self._apellido = valor if valor else ""

    # --- RUTA ---
    @property
    def ruta(self):
        return self._ruta

    @ruta.setter
    def ruta(self, valor):
        self._ruta = valor if valor else ""

    # --- COSTO ---
    @property
    def costo(self):
        return self._costo

    @costo.setter
    def costo(self, valor):
        # Aceptamos el valor tal cual, validaremos si es número en la interfaz
        self._costo = valor if valor else "0.0"

    # --- TIPO DE SERVICIO ---
    @property
    def tipo_servicio(self):
        return self._tipo_servicio

    @tipo_servicio.setter
    def tipo_servicio(self, valor):
        self._tipo_servicio = valor if valor else ""

    def __str__(self):
        return (f"Servicio: {self.nombre} {self.apellido} - Ruta: {self.ruta} (${self.costo})")