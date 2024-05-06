# !/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
from pathlib import Path

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
        self.lblDscCurso = self.create_label(frm_1, "lbldsccurso", 'Curso:', x=275, y=185)
        #Label Horario
        self.lblHorario = self.create_label(frm_1, "label3", 'Hora:', x=635, y=185)
        
    def create_label(self, parent, name, text, x, y, bold=False):
        lbl = ttk.Label(parent, name=name)
        lbl.configure(background="#f7f9fd", font=f"Arial 11 {'bold' if bold else ''}",
                      justify="left", state="normal", takefocus=False, text=text)
        lbl.place(anchor="nw", x=x, y=y)
        return lbl
    
    def create_entries(self, frm_1):
        #Entry No. Inscripción
        self.num_Inscripcion = self.create_entry(frm_1, "num_inscripcion", "right", width=100, x=682, y=42)
        # Entry Fecha
        self.fecha = self.create_entry(frm_1, "fecha", "center", width=90, x=680, y=80)
        #Combobox Alumno
        self.cmbx_Id_Alumno = self.create_combobox(frm_1, "cmbx_id_alumno", width=112, x=100, y=80)
        #Entry Alumno
        self.nombres = self.create_entry(frm_1, "nombres", None, width=200, x=100, y=130)
        #Entry Apellidos
        self.apellidos = self.create_entry(frm_1, "apellidos", None, width=200, x=485, y=130)
        #Entry Curso
        self.id_Curso = self.create_entry(frm_1, "id_curso", "left", width=166, x=100, y=185)
        #Entry de Descripción del Curso 
        self.descripc_Curso = self.create_entry(frm_1, "descripc_curso", "left", width=300, x=325, y=185)
        #Entry del Horario
        self.horario = self.create_entry(frm_1, "entry3", "left", width=100, x=680, y=185)

    def create_entry(self, parent, name, justify, width, x, y):
        entry = ttk.Entry(parent, name=name)
        if justify:
            entry.configure(justify=justify)
        entry.place(anchor="nw", width=width, x=x, y=y)
        return entry

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
        tView_cols = ['tV_descripción']
        tView_dcols = ['tV_descripción']
        tView.configure(columns=tView_cols,displaycolumns=tView_dcols)
        tView.column("#0",anchor="w",stretch=True,width=10,minwidth=10)
        tView.column("tV_descripción",anchor="w",stretch=True,width=200,minwidth=50)
        tView.heading("#0", anchor="w", text='Curso')
        tView.heading("tV_descripción", anchor="w", text='Descripción')
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

    def execute_db_query(self, query):
        """
        The function `execute_db_query` executes a given SQL query on a SQLite database and logs any
        errors encountered.
        
        :param query: The `query` parameter in the `execute_db_query` function is a SQL query that you
        want to execute on the SQLite database. This query can be any valid SQL statement such as
        SELECT, INSERT, UPDATE, DELETE, etc. The function will execute this query on the SQLite database
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
        except sqlite3.Error as e:
            logger.error("Error executing SQLite query: %s", e)
    
    def run(self):
        self.mainwindow.mainloop()


    ''' A partir de este punto se deben incluir las funciones
     para el manejo de la base de datos '''


if __name__ == "__main__":
    app = Inscripciones()
    app.run()
