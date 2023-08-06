import click
import kikit.export as kiexport
from kikit.panelize import Panel, fromMm, wxPointMM, wxRectMM, fromDegrees
from kikit.present import boardpage
from kikit.modify import references
import sys

@click.group()
def panelize():
    """
    Create a simple predefined panel patterns
    """
    pass

@click.command()
@click.argument("input", type=click.Path(dir_okay=False))
@click.argument("output", type=click.Path(dir_okay=False))
@click.option("--sourcearea", "-s", type=(float, float, float, float), help="x y w h in millimeters")
def extractBoard(input, output, sourcearea):
    """
    Extract a single board out of a file

    The extracted board is placed in the middle of the sheet
    """
    try:
        panel = Panel()
        destination = wxPointMM(150, 100)
        area = wxRectMM(*sourcearea)
        panel.appendBoard(input, destination, area, tolerance=fromMm(2))
        panel.save(output)
    except Exception as e:
        sys.stderr.write("An error occurred: " + str(e) + "\n")
        sys.stderr.write("No output files produced\n")
        sys.exit(1)

@click.command()
@click.argument("input", type=click.Path(dir_okay=False))
@click.argument("output", type=click.Path(dir_okay=False))
@click.option("--space", "-s", type=float, default=0, help="Space between boards")
@click.option("--gridsize", "-g", type=(int, int), help="Panel size <rows> <cols>")
@click.option("--panelsize", "-p", type=(float, float), help="<width> <height>", default=(None, None))
@click.option("--tabwidth", type=float, default=0,
    help="Size of the bottom/up tabs, leave unset for full width")
@click.option("--tabheight", type=float, default=0,
    help="Size of the left/right tabs, leave unset for full height")
@click.option("--htabs", type=int, default=1,
    help="Number of horizontal tabs for each board")
@click.option("--vtabs", type=int, default=1,
    help="Number of vertical tabs for each board")
@click.option("--vcuts", type=bool, help="Use V-cuts to separe the boards", is_flag=True)
@click.option("--vcutcurves", type=bool, help="Use V-cuts to approximate curves using starting and ending point", is_flag=True)
@click.option("--mousebites", type=(float, float, float), default=(None, None, None),
    help="Use mouse bites to separate the boards. Specify drill size, spacing and offset from cutedge (use 0.25 mm if unsure)")
@click.option("--radius", type=float, default=0, help="Add a radius to inner corners")
@click.option("--rotation", type=float, default=0,
    help="Rotate input board (in degrees)")
@click.option("--sourcearea", type=(float, float, float, float),
    help="x y w h in millimeters. If not specified, automatically detected", default=(None, None, None, None))
def grid(input, output, space, gridsize, panelsize, tabwidth, tabheight, vcuts,
         mousebites, radius, sourcearea, vcutcurves, htabs, vtabs, rotation):
    """
    Create a regular panel placed in a frame.

    If you do not specify the panelsize, no frame is created
    """
    try:
        panel = Panel()
        rows, cols = gridsize
        if sourcearea[0]:
            sourcearea = wxRectMM(*sourcearea)
        else:
            sourcearea = None
        if panelsize[0]:
            w, h = panelsize
            frame = True
            oht, ovt = fromMm(space), fromMm(space)
        else:
            frame = False
            oht, ovt = 0, 0
        psize, cuts = panel.makeGrid(input, rows, cols, wxPointMM(50, 50),
            sourceArea=sourcearea, tolerance=fromMm(5),
            verSpace=fromMm(space), horSpace=fromMm(space),
            verTabWidth=fromMm(tabwidth), horTabWidth=fromMm(tabheight),
            outerHorTabThickness=oht, outerVerTabThickness=ovt,
            horTabCount=htabs, verTabCount=vtabs, rotation=fromDegrees(rotation))
        panel.addMillFillets(fromMm(radius))
        if vcuts:
            panel.makeVCuts(cuts, vcutcurves)
        if mousebites[0]:
            drill, spacing, offset = mousebites
            panel.makeMouseBites(cuts, fromMm(drill), fromMm(spacing), fromMm(offset))
        if frame:
            panel.makeFrame(psize, fromMm(w), fromMm(h), fromMm(space))
        panel.save(output)
    except Exception as e:
        sys.stderr.write("An error occurred: " + str(e) + "\n")
        sys.stderr.write("No output files produced\n")
        sys.exit(1)

@click.command()
@click.argument("input", type=click.Path(dir_okay=False))
@click.argument("output", type=click.Path(dir_okay=False))
@click.option("--space", "-s", type=float, default=2, help="Space between boards")
@click.option("--slotwidth", "-w", type=float, default=2, help="Milled slot width")
@click.option("--gridsize", "-g", type=(int, int), help="Panel size <rows> <cols>")
@click.option("--panelsize", "-p", type=(float, float), help="<width> <height>", default=(None, None))
@click.option("--tabwidth", type=float, default=0,
    help="Size of the bottom/up tabs, leave unset for full width")
@click.option("--tabheight", type=float, default=0,
    help="Size of the left/right tabs, leave unset for full height")
@click.option("--htabs", type=int, default=1,
    help="Number of horizontal tabs for each board")
@click.option("--vtabs", type=int, default=1,
    help="Number of vertical tabs for each board")
@click.option("--vcuts", type=bool, help="Use V-cuts to separe the boards", is_flag=True)
@click.option("--vcutcurves", type=bool, help="Use V-cuts to approximate curves using starting and ending point", is_flag=True)
@click.option("--mousebites", type=(float, float, float), default=(None, None, None),
    help="Use mouse bites to separate the boards. Specify drill size, spacing and offset from cutedge (use 0.25 mm if unsure)")
@click.option("--radius", type=float, default=0, help="Add a radius to inner corners")
@click.option("--rotation", type=float, default=0,
    help="Rotate input board (in degrees)")
@click.option("--sourcearea", type=(float, float, float, float),
    help="x y w h in millimeters. If not specified, automatically detected", default=(None, None, None, None))
def tightgrid(input, output, space, gridsize, panelsize, tabwidth, tabheight, vcuts,
         mousebites, radius, sourcearea, vcutcurves, htabs, vtabs, rotation, slotwidth):
    """
    Create a regular panel placed in a frame by milling a slot around the
    boards' perimeters.
    """
    try:
        panel = Panel()
        rows, cols = gridsize
        if sourcearea[0]:
            sourcearea = wxRectMM(*sourcearea)
        else:
            sourcearea = None
        w, h = panelsize
        if 2 * radius > 1.1 * slotwidth:
            raise RuntimeError("The slot is too narrow for given radius (it has to be at least 10% larger")
        psize, cuts = panel.makeTightGrid(input, rows, cols, wxPointMM(50, 50),
            verSpace=fromMm(space), horSpace=fromMm(space),
            slotWidth=fromMm(slotwidth), width=fromMm(w), height=fromMm(h),
            sourceArea=sourcearea, tolerance=fromMm(5),
            verTabWidth=fromMm(tabwidth), horTabWidth=fromMm(tabheight),
            verTabCount=htabs, horTabCount=vtabs, rotation=fromDegrees(rotation))
        panel.addMillFillets(fromMm(radius))
        if vcuts:
            panel.makeVCuts(cuts, vcutcurves)
        if mousebites[0]:
            drill, spacing, offset = mousebites
            panel.makeMouseBites(cuts, fromMm(drill), fromMm(spacing), fromMm(offset))
        panel.save(output)
    except Exception as e:
        sys.stderr.write("An error occurred: " + str(e) + "\n")
        sys.stderr.write("No output files produced\n")
        sys.exit(1)

panelize.add_command(extractBoard)
panelize.add_command(grid)
panelize.add_command(tightgrid)

@click.group()
def export():
    """
    Export KiCAD boards
    """
    pass

export.add_command(kiexport.gerber)
export.add_command(kiexport.dxf)

@click.group()
def present():
    """
    Prepare board presentation
    """
    pass

present.add_command(boardpage)

@click.group()
def modify():
    """
    Modify board items
    """
    pass

modify.add_command(references)

@click.group()
def cli():
    pass
cli.add_command(export)
cli.add_command(panelize)
cli.add_command(present)
cli.add_command(modify)



if __name__ == '__main__':
    cli()
