import vtk


def write_in_file(filename, data):
    # Step 2: Sauvez le résultat au moyen d'un vtkPolyDataWriter.
    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(filename)
    writer.SetInputData(data)
    writer.Write()


def read_in_file(filename):
    # Step 3: Lisez le fichier sauvé au moyen d'un vtkPolyDataReader
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader

def init_cube(vertices):
    cube_data = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    polys = vtk.vtkCellArray()

    for i in range(len(vertices)):
        points.InsertPoint(i, vertices[i])

    return cube_data, points, polys

def cube_with_square(vertices):
    pts = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
           (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]

    cube_data, points, polys = init_cube(vertices)

    for i in range(6):
        polys.InsertNextCell(4, pts[i])

    cube_data.SetPoints(points)
    cube_data.SetPolys(polys)

    return cube_data


def cube_with_triangle(vertices):
    # Step 4: Idem mais en utilisant des 12 triangles au lieu de 6 carrés.
    pts = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 1, 5),
           (0, 4, 5), (4, 5, 6), (4, 6, 7), (3, 4, 7),
           (1, 2, 5), (2, 5, 6), (2, 3, 6), (3, 6, 7)]

    cube_data, points, polys = init_cube(vertices)

    for i in range(12):
        polys.InsertNextCell(3, pts[i])

    cube_data.SetPoints(points)
    cube_data.SetPolys(polys)

    return cube_data


def cube_with_strips():
    # We found the correct order of the points for the strips here
    # Source:
    # https://stackoverflow.com/questions/28375338/cube-using-single-gl-triangle-strip
    vertices = [(0.0, 1.0, 0.0), (1.0, 1.0, 0.0), (0.0, 0.0, 0.0), (1.0, 0.0, 0.0),
                (1.0, 0.0, 1.0), (1.0, 1.0, 0.0), (1.0, 1.0, 1.0), (0.0, 1.0, 0.0),
                (0.0, 1.0, 1.0), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 1.0),
                (0.0, 1.0, 1.0), (1.0, 1.0, 1.0)]

    points = vtk.vtkPoints()
    for i in range(len(vertices)):
        points.InsertPoint(i, vertices[i])

    triangleStrip = vtk.vtkTriangleStrip()
    triangleStrip.GetPointIds().SetNumberOfIds(14)
    for i in range(14):
        triangleStrip.GetPointIds().SetId(i, i)

    cells = vtk.vtkCellArray()
    cells.InsertNextCell(triangleStrip)

    polydata = vtk.vtkPolyData()
    # Final set before returning the object
    polydata.SetPoints(points)
    polydata.SetStrips(cells)

    return polydata


def main():
    vertices = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 1.0, 1.0), (0.0, 1.0, 1.0)]

    # Step 1
    cube_shape = cube_with_square(vertices)
    # Step 2
    # cube_shape = cube_with_triangle(vertices)
    # Step 5
    # cube_shape = cube_with_strips()

    # Step 6
    scalars = vtk.vtkFloatArray()
    for i in range(8):
        scalars.InsertTuple1(i, i)

    cube_shape.GetPointData().SetScalars(scalars)
    del scalars

    FILENAME = 'cube.vtk'
    write_in_file(FILENAME, cube_shape)
    cube_data = read_in_file(FILENAME)

    cubeMapper = vtk.vtkPolyDataMapper()
    cubeMapper.SetInputConnection(cube_data.GetOutputPort())
    cubeMapper.SetScalarRange(0, 7)

    cubeActor = vtk.vtkActor()
    cubeActor.SetMapper(cubeMapper)
    # cubeActor.GetProperty().FrontfaceCullingOn()
    # cubeActor.GetProperty().BackfaceCullingOn()

    camera = vtk.vtkCamera()
    camera.SetPosition(1, 1, 1)
    camera.SetFocalPoint(0, 0, 0)

    renderer = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    renderer.AddActor(cubeActor)
    renderer.SetActiveCamera(camera)
    renderer.ResetCamera()
    renderer.SetBackground(1, 1, 1)

    renWin.SetSize(800, 800)

    renWin.Render()
    iren.Start()


main()
