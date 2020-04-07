import vtk


def write_in_file(filename, data):
    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(filename)
    writer.SetInputData(data)
    writer.Write()


def read_in_file(filename):
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader


def cube_with_square(vertices, pts):
    cube_data = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    polys = vtk.vtkCellArray()

    for i in range(8):
        points.InsertPoint(i, vertices[i])

    for i in range(6):
        polys.InsertNextCell(4, pts[i])

    cube_data.SetPoints(points)
    cube_data.SetPolys(polys)

    return cube_data


def main():
    vertices = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 1.0, 1.0), (0.0, 1.0, 1.0)]

    pts = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
           (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]

    cube_shape = cube_with_square(vertices, pts)

    FILENAME = 'cube.vtk'
    write_in_file(FILENAME, cube_shape)
    cube_data = read_in_file(FILENAME)

    cubeMapper = vtk.vtkPolyDataMapper()
    cubeMapper.SetInputConnection(cube_data.GetOutputPort())

    cubeActor = vtk.vtkActor()
    cubeActor.SetMapper(cubeMapper)

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
