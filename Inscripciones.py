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
    def __init__(self, master=None):\
        # Ventana principal
        self.db_name = DB_PATH
        self.win = self.create_main_window(master)

        # Crea los frames
        self.frm_1 = self.create_frame(self.win)
        # Crea los labels
        self.create_labels(self.frm_1)
        #Crea los entries
        self.create_entries(self.frm_1)
        ''' Botones  de la Aplicación'''
        self.create_buttons(self.frm_1)
        # Llenar los combobox
        self.fill_cmboxes()
        #Separador
        separator1 = ttk.Separator(self.frm_1)
        separator1.configure(orient="horizontal")
        separator1.place(anchor="nw", width=796, x=2, y=245)
        ''' Treeview de la Aplicación'''
        #Treeview
        self.tView = self.create_treeview(self.frm_1)
        #Scrollbars
        self.scroll_H, self.scroll_Y = self.create_scrollbars(self.frm_1)
        self.frm_1.pack(side="top")
        self.frm_1.pack_propagate(0)
        # Main widget
        self.mainwindow = self.win

    def create_main_window(self, master):
        win = tk.Tk(master)
        win.configure(background="#f7f9fd", height=600, width=800)
        win.geometry("800x600")
        win.resizable(False, False)
        win.title("Inscripciones de Materias y Cursos")
        return win

    def create_frame(self, win, frame_name="frm_1"):
        frm_1 = tk.Frame(win, name=frame_name)
        frm_1.configure(background="#f7f9fd", height=600, width=800)
        return frm_1
    
    def create_labels(self, frm_1):
        #Label No. Inscripción
        self.lblNoInscripcion = self.create_label(frm_1, "lblnoinscripcion", 'No.Inscripción', x=680, y=20, bold=True)
        #Label Fecha
        self.lblFecha = self.create_label(frm_1, "lblfecha", 'Fecha:', x=630, y=80)
        #Label Alumno
        self.lblIdAlumno = self.create_label(frm_1, "lblidalumno", 'Id Alumno:', x=20, y=80)
        #Label Alumno
        self.lblNombres = self.create_label(frm_1, "lblnombres", 'Nombre(s):', x=20, y=130)
        #Label Apellidos
        self.lblApellidos = self.create_label(frm_1, "lblapellidos", 'Apellido(s):', x=400, y=130)
        #Label Curso
        self.lblIdCurso = self.create_label(frm_1, "lblidcurso", 'Id Curso:', x=20, y=185)
        #Label Descripción del Curso
        self.lblDscCurso = self.create_label(frm_1, "lbldsccurso", 'Curso:', x=221, y=185)
        #Label Horario
        self.lblHorario = self.create_label(frm_1, "lblhorario", 'Horario:', x=581, y=185)
        
    def create_label(self, parent, name, text, x, y, bold=False):
        lbl = ttk.Label(parent, name=name)
        lbl.configure(background="#f7f9fd", font=f"Arial 11 {'bold' if bold else ''}",
                      justify="left", state="normal", takefocus=False, text=text)
        lbl.place(anchor="nw", x=x, y=y)
        return lbl
    
    def create_entries(self, frm_1):
        #Entry No. Inscripción
        self.num_Inscripcion = self.create_combobox(frm_1, "cmbx_num_inscripcion", width=100, x=682, y=42)
        # Entry Fecha
        self.fecha = self.create_entry(frm_1, "fecha", "center", width=90, x=680, y=80)
        self.fecha.config(validate="key", validatecommand=(self.fecha.register(lambda text: len(text) < 11), "%P"))
        self.fecha.bind("<KeyRelease>",self.format_Date_Input)
        self.fecha.bind("<BackSpace>",lambda _:self.fecha.delete(len(self.fecha.get())),"end")
        self.fecha.bind("<FocusOut>", self.is_Valid_Date)
        #Combobox Alumno
        self.cmbx_Id_Alumno = self.create_combobox(frm_1, "cmbx_id_alumno", width=112, x=100, y=80)
        #Entry Alumno
        self.nombres = self.create_entry(frm_1, "nombres", None, width=200, x=100, y=130)
        #Entry Apellidos
        self.apellidos = self.create_entry(frm_1, "apellidos", None, width=200, x=485, y=130)
        #Entry Curso
        self.cmbx_Id_Curso = self.create_combobox(frm_1, "cmbx_id_curso", width=112, x=100, y=185)
        #Entry de Descripción del Curso 
        self.descripc_Curso = self.create_entry(frm_1, "descripc_curso", "left", width=300, x=271, y=185)
        #Entry del Horario
        self.horario = self.create_entry(frm_1, "horario", "left", width=140, x=640, y=185)

    def create_entry(self, parent, name, justify, width, x, y):
        entry = ttk.Entry(parent, name=name)
        if justify:
            entry.configure(justify=justify)
        entry.place(anchor="nw", width=width, x=x, y=y)
        return entry
    
    def format_Date_Input(self,event=None):
        if event.char.isdigit():
            campo=self.fecha.get()
            letras=0
            for i in campo:
                letras +=1
            if letras ==2:self.fecha.insert(2,"/")
            if letras ==5:self.fecha.insert(6,"/")
        else:
            return "break"

    def is_Valid_Date(self, _):
        while True:
            try:
                dia,mes,anio=map(int,self.fecha.get().split("/"))
                datetime(anio,mes,dia)
                
            except ValueError:
                mssg.showerror("Error fecha equivocada")
                return False

    def create_combobox(self, parent, name, width, x, y):
        cmbx = ttk.Combobox(parent, name=name)
        cmbx.place(anchor="nw", width=width, x=x, y=y)
        return cmbx
    
    def create_buttons(self, frm_1):
        #Botón Guardar
        self.btnGuardar = self.create_button(frm_1, "btnguardar", 'Guardar', x=200, y=260)
        #Botón Editar
        self.btnEditar = self.create_button(frm_1, "btneditar", 'Editar', x=300, y=260)
        #Botón Eliminar
        self.btnEliminar = self.create_button(frm_1, "btneliminar", 'Eliminar', x=400, y=260)
        #Botón Cancelar
        self.btnCancelar = self.create_button(frm_1, "btncancelar", 'Cancelar', x=500, y=260)

    def create_button(self, parent, name, text, x, y):
        btn = ttk.Button(parent, name=name)
        btn.configure(text=text)
        btn.place(anchor="nw", x=x, y=y)
        return btn
    
    def create_treeview(self, frm_1):
        tView = ttk.Treeview(frm_1, name="tview")
        tView.configure(selectmode="extended")
    
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
    
        tView.place(anchor="nw", height=300, width=790, x=4, y=300)
        return tView

    def create_scrollbars(self, frm_1):
        scroll_H = ttk.Scrollbar(frm_1, name="scroll_h")
        scroll_H.configure(orient="horizontal")
        scroll_H.place(anchor="s", height=12, width=1534, x=15, y=595)

        scroll_Y = ttk.Scrollbar(frm_1, name="scroll_y")
        scroll_Y.configure(orient="vertical")
        scroll_Y.place(anchor="s", height=275, width=12, x=790, y=582)
        return scroll_H, scroll_Y

    def fill_alumno_data(self, _):
        """
        This function is triggered when a selection is made in the 'cmbx_Id_Alumno' combobox.
        It fetches the selected student's data from the 'Alumnos' table and fills the 'nombres' and 'apellidos' fields.
    
        Args:
            _: This argument is not used in the function. It is included because this function is used as an event handler, which always receive an event object as an argument.
        """
        #  Obtain the selected student's ID
        id_alumno = self.cmbx_Id_Alumno.get()
        # Fetch the selected student's data
        alumno = self.get_one_from_table("Alumnos", "Nombres, Apellidos", ("Id_Alumno", id_alumno))
        self.nombres.delete(0, tk.END)
        self.apellidos.delete(0, tk.END)
        if len(alumno) > 0:
            self.nombres.insert(0, alumno[0])
            self.apellidos.insert(0, alumno[1])
    
    def fill_curso_data(self, _):
        """
        This function is triggered when a selection is made in the 'cmbx_Id_Curso' combobox.
        It fetches the selected course's data from the 'Cursos' table and fills the 'descripc_Curso' field.
    
        Args:
            _: This argument is not used in the function. It is included because this function is used as an event handler, which always receive an event object as an argument.
        """
        #  Obtain the selected course's ID
        id_curso = self.cmbx_Id_Curso.get()
        # Fetch the selected course's data
        curso = self.get_one_from_table("Cursos", "Descrip_Curso", ("Codigo_Curso", id_curso))
        self.descripc_Curso.delete(0, tk.END)
        if len(curso) > 0:
            self.descripc_Curso.insert(0, curso[0])
            
    def fill_inscritos(self, _):
        result = self.get_data_from_inscritos(self.num_Inscripcion.get())
        # Clear the treeView
        self.tView.delete(*self.tView.get_children())
        
        # Fill treeView with data
        for record in result:
            self.tView.insert("", tk.END, text=record.num_inscripcion, values=(record.codigo_curso, record.id_alumno, record.desc_curso, record.horario))

    
    def fill_cmboxes(self):
        """
        This function fills the 'cmbx_Id_Alumno' and 'cmbx_Id_Curso' comboboxes with data from the 'Alumnos' and 'Cursos' tables respectively.
        It also binds the '<<ComboboxSelected>>' event to the 'fill_alumno_data' and 'fill_curso_data' functions for the respective comboboxes.
        """
        # Fill the 'cmbx_Id_Alumno' combobox with data
        alumnos = self.get_all_from_table("Alumnos", "Id_Alumno")
        self.cmbx_Id_Alumno["values"] = [alumno[0] for alumno in alumnos]
        # prevent typing a value
        self.cmbx_Id_Alumno['state'] = 'readonly'
        # Bind the '<<ComboboxSelected>>' event to the 'fill_alumno_data' function
        self.cmbx_Id_Alumno.bind("<<ComboboxSelected>>", self.fill_alumno_data)

        # Fill the 'cmbx_Id_Curso' combobox with data
        cursos = self.get_all_from_table("Cursos", "Codigo_Curso")
        self.cmbx_Id_Curso["values"] = [curso[0] for curso in cursos]
        # Prevent from typing a value
        self.cmbx_Id_Curso['state'] = 'readonly'
        # Bind the '<<ComboboxSelected>>' event to the 'fill_curso_data' function
        self.cmbx_Id_Curso.bind("<<ComboboxSelected>>", self.fill_curso_data)

        # Fill the 'cmbx_num_Inscripcion' combobox with data
        inscripciones = self.get_all_from_table("Inscritos", "No_Inscripcion", group="No_Inscripcion", order="No_Inscripcion ASC")
        self.num_Inscripcion["values"] = [inscripcion[0] for inscripcion in inscripciones]
        # Prevent from typing a value
        self.num_Inscripcion['state'] = 'readonly'
        self.num_Inscripcion.bind("<<ComboboxSelected>>", self.fill_inscritos)
        
    
    def run(self):
        self.mainwindow.mainloop()


    ''' A partir de este punto se deben incluir las funciones
    para el manejo de la base de datos '''

    def execute_db_query(self, query, params=()) -> Union[sqlite3.Cursor, None]:
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

    def get_all_from_table(self, table_name, fields: str = "*", group: str = "", order: str = ""):
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
        result = self.execute_db_query(query)
        return result.fetchall() if result else []
    
    def get_one_from_table(self, table_name, fields: str = "*", where: tuple = ()):
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
        result = self.execute_db_query(query, (where[1],))
        return result.fetchone() if result else []
    
    def get_data_from_inscritos(self, num_inscripcion: int):
        # Get data from tabla Inscritos. Fields: No_Inscripcion, Codigo_Curso, Id_Alumno, Descrip_Curso, Horario
        query = """
        SELECT i.No_Inscripcion, i.Id_Alumno, i.Fecha_Inscripcion, i.Codigo_Curso, c.Descrip_Curso, i.Horario 
        FROM Inscritos i 
        JOIN Cursos c ON i.Codigo_Curso = c.Codigo_Curso 
        WHERE i.No_Inscripcion = ?
        """	
        # Execute the query and get object instances from the result
        result = self.execute_db_query(query, (num_inscripcion,))
        return [Inscritos(*record) for record in result.fetchall()] if result else []


class Inscritos:
    table_Name = "Inscritos"
    def __init__(self, num_inscripcion: int, id_alumno: str, fecha: datetime, codigo_curso: str, desc_curso:str, horario: str):
        self.num_inscripcion = num_inscripcion
        self.id_alumno = id_alumno
        self.fecha = fecha
        self.codigo_curso = codigo_curso
        self.desc_curso = desc_curso
        self.horario = horario
        

if __name__ == "__main__":
    app = Inscripciones()
    app.run()
