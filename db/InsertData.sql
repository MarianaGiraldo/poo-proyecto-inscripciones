-- Comando para eliminar todos los registros de las tablas Alumnos, Carreras y Cursos
DELETE FROM Alumnos;
DELETE FROM Carreras;
DELETE FROM Cursos;
-- Comando para insertar registros en la tabla Carreras
INSERT INTO Carreras (Codigo_Carrera, Descripcion, Num_Semestres)
VALUES 
    ('ING_SIS', 'Ingeniería de Sistemas y Computación', 10),
    ('ADM_EMP', 'Administración de Empresas', 8),
    ('DER', 'Derecho', 10),
    ('MED', 'Medicina', 12),
    ('ARQ', 'Arquitectura', 10),
    ('EDU', 'Educación', 8),
    ('CON', 'Contabilidad', 8),
    ('ING_ELE', 'Ingeniería Eléctrica', 10),
    ('PSI', 'Psicología', 8),
    ('ING_IND', 'Ingeniería Industrial', 10);

-- Comando para insertar registros en la tabla Alumnos
INSERT INTO Alumnos (Id_Alumno, Id_Carrera, Nombres, Apellidos, Fecha_Ingreso, Direccion, Telef_Cel, Telef_Fijo, Ciudad, Departamento)
VALUES 
    ('1032793456', 'ING_SIS', 'Mariana', 'Giraldo Luna', '2024-01-30', 'Cra 31a #30a-90', '3057964568', '8933796', 'Cali', 'Valle del Cauca'),
    ('1093723491', 'ADM_EMP', 'Carlos', 'Gomez Perez', '2023-05-15', 'Calle 45 #20-30', '3109876543', '8765432', 'Bogotá', 'Cundinamarca'),
    ('1029387856', 'DER', 'Laura', 'Martinez Ramirez', '2022-11-20', 'Av. 5 #10-15', '3151234567', '9123456', 'Medellín', 'Antioquia'),
    ('1237654321', 'MED', 'Javier', 'Sanchez Diaz', '2021-07-10', 'Carrera 8 #15-40', '3202345678', '7654321', 'Barranquilla', 'Atlántico'),
    ('1098767892', 'ARQ', 'Ana', 'Gonzalez Rodriguez', '2020-03-25', 'Calle 20 #40-50', '3003456789', '6543210', 'Cartagena', 'Bolívar'),
    ('1089382716', 'EDU', 'Pedro', 'Lopez Gomez', '2019-09-05', 'Av. 10 #25-35', '3054567890', '5432109', 'Pasto', 'Nariño'),
    ('1019283786', 'CON', 'Sofia', 'Hernandez Gutierrez', '2018-04-12', 'Carrera 15 #30-20', '3105678901', '4321098', 'Cúcuta', 'Norte de Santander'),
    ('1062543789', 'ING_ELE', 'Andres', 'Perez Garcia', '2017-12-03', 'Calle 35 #15-25', '3206789012', '3210987', 'Pereira', 'Risaralda'),
    ('1073564291', 'PSI', 'Camila', 'Diaz Hernandez', '2016-08-18', 'Av. 20 #35-45', '3157890123', '2109876', 'Manizales', 'Caldas'),
    ('1029384446', 'ING_IND', 'Juan', 'Gomez Perez', '2015-02-27', 'Cra 10 #20-30', '3009012345', '1098765', 'Santa Marta', 'Magdalena');

-- Comando para insertar registros en la tabla Cursos
INSERT INTO Cursos (Codigo_Curso, Descrip_Curso, Num_Horas)
VALUES 
    ('TGS_1', 'Teoría General de Sistemas', 4),
    ('MAT_BAS', 'Matemáticas Básicas', 6),
    ('ADM_FIN', 'Administración Financiera', 5),
    ('FIS_1', 'Física I', 4),
    ('ECO_MIC', 'Economía Microeconómica', 5),
    ('COMP_PROG', 'Programación de Computadoras', 6),
    ('ADM_EMP', 'Administración de Empresas', 5),
    ('PSI_SOC', 'Psicología Social', 4),
    ('ING_SOFT', 'Ingeniería de Software', 6),
    ('DER_CIV', 'Derecho Civil', 5);
