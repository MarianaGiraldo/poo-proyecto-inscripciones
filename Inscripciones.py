# !/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mssg
import sqlite3
from pathlib import Path
from typing import Union
from datetime import datetime

logger = logging.getLogger(__name__)
PATH = str((Path(__file__).resolve()).parent)
DB_PATH = f"{PATH}/db/Inscripciones.db"

class Inscripciones:
    def __init__(self, master=None):
        # Ventana principal
        self.db_name = DB_PATH
        self.win = self.create_Main_Window(master)
        win_width = 800
        win_height = 600

        # Obtener la resolución de la pantalla
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()

        # Calcular las coordenadas x e y para centrar la ventana
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2

        # Establecer la geometría de la ventana
        self.win.geometry(f'{win_width}x{win_height}+{x}+{y}')

        # Crea los frames
        self.frm_1 = self.create_Frame(self.win)
        # Crea los labels
        self.create_Labels(self.frm_1)
        #Crea los entries
        self.create_Entries(self.frm_1)
        ''' Botones  de la Aplicación'''
        self.create_Buttons(self.frm_1)
        # Llenar los combobox
        self.fill_Cmboxes()
        #Separador
        separator1 = ttk.Separator(self.frm_1)
        separator1.configure(orient="horizontal")
        separator1.place(anchor="nw", width=796, x=2, y=245)
        ''' Treeview de la Aplicación'''
        #Treeview
        self.tView = self.create_Treeview(self.frm_1)
        #Scrollbars
        self.scroll_H, self.scroll_Y = self.create_Scrollbars(self.frm_1)
        self.frm_1.pack(side="top")
        self.frm_1.pack_propagate(0)
        # Main widget
        self.mainwindow = self.win
        self.crear_Estilos()

    def create_Main_Window(self, master):
        win = tk.Tk(master)
        win.configure(background="#f7f9fd", height=600, width=800)
        win.geometry("800x600")
        win.resizable(False, False)
        win.iconbitmap(f"{PATH}/img/icon.ico")
        win.title("Inscripciones de Materias y Cursos")
        return win

    def create_Frame(self, win, frame_name="frm_1"):
        frm_1 = tk.Frame(win, name=frame_name)
        frm_1.configure(height=600, width=800)
        return frm_1

    def create_Labels(self, frm_1):
        #Label No. Inscripción
        self.lblNoInscripcion = self.create_Label(frm_1, "lblnoinscripcion", 'No.Inscripción', x=680, y=20, bold=True)
        #Label Fecha
        self.lblFecha = self.create_Label(frm_1, "lblfecha", 'Fecha:', x=630, y=80)
        #Label Alumno
        self.lblIdAlumno = self.create_Label(frm_1, "lblidalumno", 'Id Alumno:', x=20, y=80)
        #Label Alumno
        self.lblNombres = self.create_Label(frm_1, "lblnombres", 'Nombre(s):', x=20, y=130)
        #Label Apellidos
        self.lblApellidos = self.create_Label(frm_1, "lblapellidos", 'Apellido(s):', x=400, y=130)
        #Label Curso
        self.lblIdCurso = self.create_Label(frm_1, "lblidcurso", 'Id Curso:', x=20, y=185)
        #Label Descripción del Curso
        self.lblDscCurso = self.create_Label(frm_1, "lbldsccurso", 'Curso:', x=221, y=185)
        #Label Horario
        self.lblHorario = self.create_Label(frm_1, "lblhorario", 'Horario:', x=501, y=185)
        self.lblHorario_hasta = self.create_Label(frm_1, "lblhorario_hasta", 'a', x=670, y=185)

    def create_Label(self, parent, name, text, x, y, bold=False):
        lbl = ttk.Label(parent, name=name)
        lbl.configure(font=f"Arial 11 {'bold' if bold else ''}",
                      justify="left", state="normal", takefocus=False, text=text)
        lbl.place(anchor="nw", x=x, y=y)
        return lbl

    def create_Entries(self, frm_1):
        #Entry No. Inscripción
        self.num_Inscripcion = self.create_Combobox(frm_1, "cmbx_num_inscripcion", width=100, x=682, y=42)
        # Entry Fecha
        self.fecha = self.create_Entry(frm_1, "fecha", "center", width=90, x=680, y=80)
        self.fecha.config(validate="key", validatecommand=(self.fecha.register(lambda text: len(text) < 11), "%P"))
        self.fecha.bind("<KeyRelease>",self.format_Date_Input)
        self.fecha.bind("<BackSpace>",lambda _:self.fecha.delete(len(self.fecha.get())),"end")
        self.fecha.bind("<FocusOut>", self.is_Valid_Date)
        #Combobox Alumno
        self.cmbx_Id_Alumno = self.create_Combobox(frm_1, "cmbx_id_alumno", width=112, x=100, y=80)
        #Entry Alumno
        self.nombres = self.create_Entry(frm_1, "nombres", None, width=200, x=100, y=130)
        #Entry Apellidos
        self.apellidos = self.create_Entry(frm_1, "apellidos", None, width=200, x=485, y=130)
        #Entry Curso
        self.cmbx_Id_Curso = self.create_Combobox(frm_1, "cmbx_id_curso", width=112, x=100, y=185)
        #Entry de Descripción del Curso
        self.descripc_Curso = self.create_Entry(frm_1, "descripc_curso", "left", width=220, x=271, y=185)
        #Entry del Horario
        self.horario_desde = self.create_Combobox(frm_1, "cmbx_horario_desde", width=60, x=560, y=185)
        self.horario_desde_am = self.create_Combobox(frm_1, "cmbx_horario_desde_am", width=40, x=625, y=185)
        self.horario_hasta = self.create_Combobox(frm_1, "cmbx_horario_hasta", width=60, x=685, y=185)
        self.horario_hasta_am = self.create_Combobox(frm_1, "cmbx_horario_hasta_am", width=40, x=750, y=185)

    def create_Entry(self, parent, name, justify, width, x, y):
        entry = ttk.Entry(parent, name=name)
        if justify:
            entry.configure(justify=justify)
        entry.place(anchor="nw", width=width, x=x, y=y)
        return entry

    def format_Date_Input(self,  event=None):
        if event.char.isdigit():
            campo=self.fecha.get()
            letras=0
            for _ in campo:
                letras +=1
            if letras ==2:self.fecha.insert(2,"/")
            if letras ==5:self.fecha.insert(6,"/")
        elif event.char.isspace():
            self.fecha.delete(len(self.fecha.get()) - 1)
        else:
            return "break"

    def is_Valid_Date(self, _):
        while True:
            try:
                dia,mes,anio=map(int,self.fecha.get().split("/"))
                datetime(anio,mes,dia)
                return True

            except ValueError:
                mssg.showerror("Error", "Error fecha equivocada")
                return False

    def create_Combobox(self, parent, name, width, x, y):
        cmbx = ttk.Combobox(parent, name=name)
        cmbx.place(anchor="nw", width=width, x=x, y=y)
        # Prevent from typing a value
        cmbx['state'] = 'readonly'
        cmbx.configure(justify="center", font="Arial 11", background="white", foreground="black")
        return cmbx

    def create_Buttons(self, frm_1):
        # Botón de nueva inscripción
        self.btnNuevaInscripcion = self.create_Button(frm_1, "btnnuevainscripcion", 'Nueva Inscripción', x=550, y=37, command=self.nueva_Inscripcion)
        #Botón Consultar
        self.btnConsultar = self.create_Button(frm_1, "btnconsultar", 'Consultar', x=100, y=260,command=self.consultar_Inscripcion)
        #Botón Guardar
        self.btnGuardar = self.create_Button(frm_1, "btnguardar", 'Guardar', x=225, y=260,command=self.crear_Inscripcion)
        #Botón Editar
        self.btnEditar = self.create_Button(frm_1, "btneditar", 'Editar', x=350, y=260,command=self.actualizar_Inscripcion)
        #Botón Eliminar
        self.btnEliminar = self.create_Button(frm_1, "btneliminar", 'Eliminar', x=475, y=260,command=self.eliminar_Inscripcion)
        #Botón Cancelar
        self.btnCancelar = self.create_Button(frm_1, "btncancelar", 'Cancelar', x=600, y=260,command=self.cancel_Operation)

    def create_Button(self, parent, name, text, x, y, command = (lambda: None)):
        btn = ttk.Button(parent, name=name, text=text, command=command)
        btn.place(anchor="nw", x=x, y=y)
        return btn

    def create_Treeview(self, frm_1):
        tView = ttk.Treeview(frm_1, name="tview", style="mystyle.Treeview", selectmode="browse")

        config_map = {
            "#0": {"width": 7, "minwidth": 7, "heading": '# Inscripción'},
            "curso": {"width": 30, "minwidth": 20, "heading": 'Curso'},
            "id_alumno": {"width": 30, "minwidth": 20, "heading": 'Id Alumno'},
            "tV_descripción": {"width": 50, "minwidth": 30, "heading": 'Descripción'},
            "horario": {"width": 30, "minwidth": 20, "heading": 'Horario'}
        }

        cols = list(config_map.keys())
        tView.configure(columns=cols[1:], displaycolumns=cols[1:])

        for col, config in config_map.items():
            tView.column(col, anchor="w", stretch=True, width=config["width"], minwidth=config["minwidth"])
            tView.heading(col, anchor="w", text=config["heading"])

        tView.place(anchor="nw", height=300, width=790, x=4, y=320)
        return tView

    def create_Scrollbars(self, frm_1):
        scroll_H = ttk.Scrollbar(frm_1, name="scroll_h")
        scroll_H.configure(orient="horizontal")
        scroll_H.place(anchor="s", height=12, width=1534, x=15, y=595)

        scroll_Y = ttk.Scrollbar(frm_1, name="scroll_y")
        scroll_Y.configure(orient="vertical")
        scroll_Y.place(anchor="s", height=275, width=12, x=790, y=582)
        return scroll_H, scroll_Y

    def fill_Alumno_Data(self, _):
        """
        This function is triggered when a selection is made in the 'cmbx_Id_Alumno' combobox.
        It fetches the selected student's data from the 'Alumnos' table and fills the 'nombres' and 'apellidos' fields.

        Args:
            _: This argument is not used in the function. It is included because this function is used as an event handler, which always receive an event object as an argument.
        """
        #  Obtain the selected student's ID
        id_alumno = self.cmbx_Id_Alumno.get()
        # Fetch the selected student's data
        alumno = self.get_One_From_Table("Alumnos", "Nombres, Apellidos", ("Id_Alumno", id_alumno))
        self.nombres.delete(0, tk.END)
        self.apellidos.delete(0, tk.END)
        if len(alumno) > 0:
            self.nombres.insert(0, alumno[0])
            self.apellidos.insert(0, alumno[1])

    def fill_Curso_Data(self, _):
        """
        This function is triggered when a selection is made in the 'cmbx_Id_Curso' combobox.
        It fetches the selected course's data from the 'Cursos' table and fills the 'descripc_Curso' field.

        Args:
            _: This argument is not used in the function. It is included because this function is used as an event handler, which always receive an event object as an argument.
        """
        #  Obtain the selected course's ID
        id_curso = self.cmbx_Id_Curso.get()
        # Fetch the selected course's data
        curso = self.get_One_From_Table("Cursos", "Descrip_Curso", ("Codigo_Curso", id_curso))
        self.descripc_Curso.delete(0, tk.END)
        if len(curso) > 0:
            self.descripc_Curso.insert(0, curso[0])

    def fill_Inscritos(self, _):
        result = self.get_Data_From_Inscritos(self.num_Inscripcion.get())
        # Clear the treeView
        self.tView.delete(*self.tView.get_children())

        # Fill treeView with data
        for record in result:
            self.tView.insert("", tk.END, text=record[0], values=(record[3], record[1], record[4], record[5]))

    def fill_Cmboxes(self):
        """
        This function fills the 'cmbx_Id_Alumno' and 'cmbx_Id_Curso' comboboxes with data from the 'Alumnos' and 'Cursos' tables respectively.
        It also binds the '<<ComboboxSelected>>' event to the 'fill_alumno_data' and 'fill_curso_data' functions for the respective comboboxes.
        """
        # Fill the 'cmbx_Id_Alumno' combobox with data
        alumnos = self.get_All_From_Table("Alumnos", "Id_Alumno")
        self.cmbx_Id_Alumno["values"] = [alumno[0] for alumno in alumnos]
        # Bind the '<<ComboboxSelected>>' event to the 'fill_alumno_data' function
        self.cmbx_Id_Alumno.bind("<<ComboboxSelected>>", self.fill_Alumno_Data)

        # Fill the 'cmbx_Id_Curso' combobox with data
        cursos = self.get_All_From_Table("Cursos", "Codigo_Curso")
        self.cmbx_Id_Curso["values"] = [curso[0] for curso in cursos]
        # Bind the '<<ComboboxSelected>>' event to the 'fill_curso_data' function
        self.cmbx_Id_Curso.bind("<<ComboboxSelected>>", self.fill_Curso_Data)

        # Fill the 'cmbx_num_Inscripcion' combobox with data
        inscripciones = self.get_All_From_Table("Inscritos", "No_Inscripcion", group="No_Inscripcion", order="No_Inscripcion ASC")
        self.num_Inscripcion["values"] = [inscripcion[0] for inscripcion in inscripciones]
        self.num_Inscripcion.bind("<<ComboboxSelected>>", self.fill_Inscritos)

        horas_del_dia = ["01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00"]
        am_pm = ["AM", "PM"]
        self.horario_desde["values"] = horas_del_dia
        self.horario_hasta["values"] = horas_del_dia
        self.horario_desde_am["values"] = am_pm
        self.horario_hasta_am["values"] = am_pm
        self.horario_desde.bind("<<ComboboxSelected>>", self.validate_Horario)
        self.horario_hasta.bind("<<ComboboxSelected>>", self.validate_Horario)
        self.horario_desde_am.bind("<<ComboboxSelected>>", self.validate_Horario)
        self.horario_hasta_am.bind("<<ComboboxSelected>>", self.validate_Horario)

    def show_Error_Horario(self):
        mssg.showerror("Error", "La hora de inicio debe ser menor que la hora de finalización")

    def validate_Horario(self, _):
        """
        This function validates the 'horario' field to ensure that the 'horario_desde' value is less than the 'horario_hasta' value.
        """
        horario_desde = self.horario_desde.get()
        horario_desde_am = self.horario_desde_am.get()
        horario_hasta = self.horario_hasta.get()
        horario_hasta_am = self.horario_hasta_am.get()

        if horario_desde == "12:00":
            self.horario_desde_am.set("M")
            if horario_hasta_am == "AM":
                self.show_Error_Horario()
                return False

        if horario_hasta == "12:00":
            self.horario_hasta_am.set("M")
            if horario_desde_am == "PM":
                self.show_Error_Horario()
                return False

        if all([horario_desde, horario_desde_am, horario_hasta, horario_hasta_am]):
            if (horario_desde_am == horario_hasta_am and horario_desde >= horario_hasta) or (horario_desde_am == "PM" and horario_hasta_am == "AM"):
                self.show_Error_Horario()
                return False

        return True

    def get_Horario(self):
        """
        This function retrieves the 'horario' value from the 'horario_desde' and 'horario_hasta' comboboxes.
        """
        if not all([self.horario_desde.get(), self.horario_desde_am.get(), self.horario_hasta.get(), self.horario_hasta_am.get()]):
            return ""
        horario_desde = self.horario_desde.get() + " " + self.horario_desde_am.get()
        horario_hasta = self.horario_hasta.get() + " " + self.horario_hasta_am.get()
        return f"{horario_desde} - {horario_hasta}"

    def nueva_Inscripcion(self):
        """
        This function is triggered when the 'Nueva Inscripción' button is clicked.
        It clears the entries and comboboxes to allow the user to create a new registration.
        """
        self.num_Inscripcion.set(self.get_Next_Inscripcion())
        self.tView.delete(*self.tView.get_children())

    def cancel_Operation(self):
        fields = [self.fecha, self.nombres, self.apellidos, self.cmbx_Id_Curso, self.descripc_Curso, self.num_Inscripcion, self.horario_desde, self.horario_desde_am, self.horario_hasta, self.horario_hasta_am]
        has_Data = any(field.get() != "" for field in fields)

        if  has_Data:
            self.create_Entries(self.frm_1)
            self.fill_Cmboxes()
            self.tView = self.create_Treeview(self.frm_1)

            mssg.showinfo("Cancelar operacion", "Operacion(es) cancelada(s)")
        else:
            mssg.showerror("Cancelar operacion", "No hay operacion(es) para cancelar")

    def desactivar_Campos(self):
        # Disable all entry fields
        self.num_Inscripcion.config(state="disabled")
        self.cmbx_Id_Alumno.config(state="disabled")
        self.nombres.config(state="disabled")
        self.apellidos.config(state="disabled")
        self.cmbx_Id_Curso.config(state="disabled")
        self.descripc_Curso.config(state="disabled")

    def consultar_Inscripcion(self):
        item_click = self.tView.focus()
        item_values = self.tView.item(item_click, "values")
        if len(item_values) == 0:
            mssg.showerror("Error", "No se ha seleccionado ninguna inscripción para consultar")
            return
        cod_curso, id_alumno = item_values[0], item_values[1]
        num_inscripcion = self.num_Inscripcion.get()
        result = self.leer_Inscrito(num_inscripcion, cod_curso, id_alumno)
        if result is None or len(result) == 0:
            mssg.showerror("Inscripción no encontrada",
                          f"No se encontró una inscripción con el número: {num_inscripcion}")
            return
        fecha, horario = result[2], result[4]
        if len(result) > 0:
            # Clean all entries
            self.create_Entries(self.frm_1)
            # Llenar los combobox
            self.fill_Cmboxes()
            self.num_Inscripcion.set(num_inscripcion)
            self.cmbx_Id_Alumno.set(id_alumno)
            self.fill_Alumno_Data(None)
            self.cmbx_Id_Curso.set(cod_curso)
            self.fill_Curso_Data(None)
            self.fecha.insert(0, fecha)
            self.horario_desde.set(horario[0:5])
            self.horario_desde_am.set(horario[6:8])
            self.horario_hasta.set(horario[11:16])
            self.horario_hasta_am.set(horario[17:19])
            self.desactivar_Campos()
        else:
            mssg.showinfo("Inscripción no encontrada",
                          f"No se encontró una inscripción con el número: {num_inscripcion}")
            
    def eliminar_Inscripcion(self):
        self.op= tk.StringVar()
        self.opcion_Eliminar()
        self.eliminar()

    def opcion_Eliminar(self):
        self.eliminar_window = tk.Toplevel(self.win)
        self.eliminar_window.title('Eliminar Datos')
        new_win_width = 220
        new_win_height = 180
        # Obtener la resolución de la pantalla
        screen_width = self.eliminar_window.winfo_screenwidth()
        screen_height = self.eliminar_window.winfo_screenheight()

        # Calcular las coordenadas x e y para centrar la ventana
        x = (screen_width - new_win_width) // 2
        y = (screen_height - new_win_height) // 2

        # Establecer la geometría de la ventana
        self.eliminar_window.geometry(f'{new_win_width}x{new_win_height}+{x}+{y}')
        self.frame=tk.Frame(self.eliminar_window,borderwidth=2,relief="groove")
        self.frame.pack(padx=10,pady=10)
        self.var=tk.StringVar()
        self.var.set(None)
        ttk.Radiobutton(self.frame,text="Eliminar uno",variable=self.var,value=1).pack(anchor='w')
        ttk.Radiobutton(self.frame,text="Eliminar todos",variable=self.var,value=2).pack(anchor='w')
        ttk.Button(self.eliminar_window, text="Aceptar", command=self.eliminar).pack()
        ttk.Button(self.eliminar_window, text="Cancelar", command=self.eliminar_window.destroy).pack()

    def crear_Estilos(self):
        style = ttk.Style(self.win)
        # Update the default settings for all widgets
        style.theme_use("clam")
        # Update frame background color
        self.frm_1.configure(background="#ECF5FE")

        # Styles for the treeview
        style.configure("Treeview", font=("Arial", 10), rowheight=25, foreground="black", background="#FFFEE0")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#7AB0CD", relief="flat")

        # Styles for the buttons
        style.configure('TButton', font =
                    ('calibri', 11, 'bold'),
                            borderwidth = '4', padding=2, relief="flat", background="#B6D8F6", foreground="black")
        style.map('TButton', background = [('active', '#7AB0CD')])

        # Styles for the comboboxes
        style.configure("TCombobox", font=("Arial", 1), background="white", foreground="black")

        style.map('TCombobox', fieldbackground=[('readonly','white')])
        style.map('TCombobox', selectbackground=[('readonly', 'white')])
        style.map('TCombobox', selectforeground=[('readonly', 'black')])


        # Scrollbar styles
        style.configure("Vertical.TScrollbar", gripcount=0,
            background="#36494E"
        )

        # Label styles
        style.configure("TLabel", background="#ECF5FE", foreground="black")

    def run(self):
        self.mainwindow.mainloop()


    ''' A partir de este punto se deben incluir las funciones
    para el manejo de la base de datos '''

    def execute_DB_Query(self, query, params=()) -> Union[sqlite3.Cursor, None]:
        """
        Executes a database query and returns the result.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): The parameters to be used in the query. Defaults to ().

        Returns:
            Union[sqlite3.Cursor, None]: The result of the query as a cursor object, or None if an error occurred.
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                result = cursor.execute(query, params)
                conn.commit()
                return result
        except sqlite3.Error as e:
            logger.error("Error executing SQLite query: %s", e)
        return None

    def get_All_From_Table(self, table_name, fields: str = "*", group: str = "", order: str = ""):
        """
        Retrieves all records from a specified table in the database.

        Args:
            table_name (str): The name of the table to retrieve records from.
            fields (str, optional): The fields to retrieve from the table. Defaults to "*".

        Returns:
            list: A list of records retrieved from the table. Each record is represented as a tuple.
        """
        query = f"SELECT {fields} FROM {table_name}"
        if group != "":
            query += f" GROUP BY {group}"
        if order != "":
            query += f" ORDER BY {order}"
        result = self.execute_DB_Query(query)
        return result.fetchall() if result else []

    def get_One_From_Table(self, table_name, fields: str = "*", where: tuple = ()):
        """
        Retrieves a single row from the specified table based on the given conditions.

        Args:
            table_name (str): The name of the table to retrieve data from.
            fields (str, optional): The fields to retrieve from the table. Defaults to "*".
            where (tuple, optional): A tuple representing the condition to filter the data.
                                    The first element is the column name and the second element is the value to match.
                                    Defaults to an empty tuple.

        Returns:
            tuple: A single row from the table that matches the given conditions, or an empty list if no match is found.
        """
        query = f"SELECT {fields} FROM {table_name} WHERE {where[0]} = ?"
        result = self.execute_DB_Query(query, (where[1],))
        return result.fetchone() if result else []

    def get_Data_From_Inscritos(self, num_inscripcion: int):
        # Get data from tabla Inscritos. Fields: No_Inscripcion, Codigo_Curso, Id_Alumno, Descrip_Curso, Horario
        query = """
        SELECT i.No_Inscripcion, i.Id_Alumno, i.Fecha_Inscripcion, i.Codigo_Curso, c.Descrip_Curso, i.Horario
        FROM Inscritos i
        JOIN Cursos c ON i.Codigo_Curso = c.Codigo_Curso
        WHERE i.No_Inscripcion = ?
        """
        # Execute the query and get object instances from the result
        result = self.execute_DB_Query(query, (num_inscripcion,))
        return result.fetchall() if result else []
        # return [Inscritos(*record) for record in result.fetchall()] if result else []

    def get_Next_Inscripcion(self):
        """
        Retrieves the next available 'No_Inscripcion' value from the 'Inscritos' table.

        Returns:
            int: The next available 'No_Inscripcion' value.
        """
        query = "SELECT MAX(No_Inscripcion) FROM Inscritos"
        result = self.execute_DB_Query(query)
        num_Inscripcion = result.fetchone()[0]
        return num_Inscripcion + 1 if num_Inscripcion else 1

    def eliminar(self):
        eleccion=self.var.get()
        if eleccion is not None:
            if eleccion=='1':
                try:
                    num_inscripcion = self.num_Inscripcion.get()
                    id_alumno = self.cmbx_Id_Alumno.get()
                    codigo_curso = self.cmbx_Id_Curso.get()
                    query = "DELETE FROM Inscritos WHERE No_Inscripcion = ? AND Id_Alumno=? AND Codigo_Curso=?"
                    params = (num_inscripcion, id_alumno, codigo_curso)
                    self.execute_DB_Query(query, params)
                    self.fill_Inscritos(None)  # Actualiza la vista del treeview
                except IndexError:
                    mssg.showerror("Error")
                finally:
                    self.eliminar_window.destroy()
            elif eleccion=='2':
                try:
                    num_inscripcion = self.num_Inscripcion.get()
                    query = "DELETE FROM Inscritos WHERE No_Inscripcion = ? "
                    self.execute_DB_Query(query, (num_inscripcion,))
                    self.fill_Inscritos(None)  # Actualiza la vista del treeview
                    self.num_Inscripcion.set("")
                    self.fill_Cmboxes()
                except IndexError:
                    mssg.showerror("Error")
                finally:
                    self.eliminar_window.destroy()

    def crear_Inscripcion(self):
        num_inscripcion = self.num_Inscripcion.get()
        id_alumno = self.cmbx_Id_Alumno.get()
        codigo_curso = self.cmbx_Id_Curso.get()
        horario = self.get_Horario()
        fecha_Inscripcion =self.fecha.get()

        query = "INSERT INTO Inscritos (No_Inscripcion, Codigo_Curso, Id_Alumno, Horario, Fecha_Inscripcion) VALUES (?, ?, ?, ?, ?)"
        params = (num_inscripcion, codigo_curso, id_alumno, horario, fecha_Inscripcion)
        if all([num_inscripcion, id_alumno, codigo_curso, horario, fecha_Inscripcion]) and self.validate_Horario(None) and self.is_Valid_Date(None):
            result = self.execute_DB_Query(query, params)
            if result:
                mssg.showinfo("Inscripción creada", "La inscripción se ha creado exitosamente")
                self.fill_Inscritos(None) # Actualiza la vista del treeview
            else:
                mssg.showerror("ERROR", "No se ha podido crear la inscripcion")
        else:
            mssg.showerror("ERROR", "No se ha podido crear la inscripcion, faltan datos")

    def leer_Inscrito(self, num_inscripcion, cod_curso, id_alumno):
        query = "SELECT * FROM Inscritos WHERE No_Inscripcion = ? AND Codigo_Curso = ? AND Id_Alumno = ?"
        result = self.execute_DB_Query(query, (num_inscripcion, cod_curso, id_alumno))
        return result.fetchone()
    
    def leer_Alumnos(self, id_alumno):
        query = "SELECT * FROM Alumnos WHERE Id_Alumno = ? "
        result = self.execute_DB_Query(query, (id_alumno,))
        return result.fetchall()

    def actualizar_Inscripcion(self):
        num_inscripcion = self.num_Inscripcion.get()
        id_alumno = self.cmbx_Id_Alumno.get()
        codigo_curso = self.cmbx_Id_Curso.get()
        horario = self.get_Horario()
        fecha_Inscripcion=self.fecha.get()
        query = "UPDATE Inscritos SET Horario = ?, Fecha_Inscripcion = ? WHERE No_Inscripcion = ? AND Id_Alumno=? AND Codigo_Curso=?"
        params = ( horario,fecha_Inscripcion,num_inscripcion,  id_alumno,codigo_curso )
        if all([num_inscripcion, id_alumno, codigo_curso, horario, fecha_Inscripcion]) and self.validate_Horario(None) and self.is_Valid_Date(None):
            result = self.execute_DB_Query(query, params)
            if result:
                mssg.showinfo("Inscripción actualizada", "La inscripción se ha actualizado exitosamente")
                self.fill_Inscritos(None)  # Actualiza la vista del treeview
            else:
                mssg.showerror("ERROR", "No se ha podido actualizar informacion")
        else:
            mssg.showerror("ERROR", "No se ha podido actualizar informacion, faltan datos")

# class Inscritos:
#     table_Name = "Inscritos"
#     def __init__(self, num_inscripcion: int, id_alumno: str, fecha: datetime, codigo_curso: str, desc_curso:str, horario: str):
#         self.num_inscripcion = num_inscripcion
#         self.id_alumno = id_alumno
#         self.fecha = fecha
#         self.codigo_curso = codigo_curso
#         self.desc_curso = desc_curso
#         self.horario = horario


if __name__ == "__main__":
    app = Inscripciones()
    app.run()
