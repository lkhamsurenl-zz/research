import datetime
import sys

from matplotlib.backends.backend_pdf import PdfPages

from src.model.grid import Grid
from src.view.genus_boundary import get_vertex_mapping, get_face_mapping
from src.algorithms.holy_tree import move_around_face

def main():
    m, n = 6, 6
    # Set deeper recursion level to avoid max recursion depth exceeded.
    if m > 5 or n > 5:
        sys.setrecursionlimit(10000)

    grid = Grid(2, m, n)

    # Get vertices in the boundary face.
    vertices = grid.get_vertices([(1, 1), (0, 1), (0, 0), (1, 0)])

    # Create a new pdf file with current timestamp.
    now = datetime.datetime.now()
    # primal_pdf = PdfPages('../../resources/{}-primal.pdf'.format(now.strftime("%m-%d-%H:%M")))
    # dual_pdf = PdfPages('../../resources/{}-dual.pdf'.format(now.strftime("%m-%d-%H:%M")))
    primal_pdf = None
    dual_pdf = None

    vertex_mapping = get_vertex_mapping(grid.genus, grid.width, grid.height)
    face_mapping = get_face_mapping(grid.genus, grid.width, grid.height)

    # Wrap all visualization related parameters in tuple.
    visual_params = (vertex_mapping, face_mapping, primal_pdf, dual_pdf)

    move_around_face(grid, vertices, visual_params)

    # Close the pdf files, if created.
    if primal_pdf is not None:
        primal_pdf.close()
    if dual_pdf is not None:
        dual_pdf.close()

if __name__ == '__main__':
    main()