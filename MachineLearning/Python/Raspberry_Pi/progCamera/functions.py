import CylinderFinder
import TennisBallFinder
import RobotsFinder
import PerspectiveTransformer


def initProcessors():

    frameProcessors = {}
    
    frameProcessors["cylindersYellow"] = CylinderFinder.CylinderFinder()
    frameProcessors["cylindersYellow"].loadParamFromFile(0)

    frameProcessors["cylindersGreen"] = CylinderFinder.CylinderFinder()
    frameProcessors["cylindersGreen"].loadParamFromFile(1)

    frameProcessors["tennisBall"] = TennisBallFinder.TennisBallFinder()
    frameProcessors["tennisBall"].loadParamFromFile()

    frameProcessors["robots"] = RobotsFinder.RobotsFinder(0)
    frameProcessors["robots"].loadParamFromFile()

    perspectiveTransformer = PerspectiveTransformer.PerspectiveTransformer()
    perspectiveTransformer.loadParamFromFile()


    return frameProcessors, perspectiveTransformer


def findObjects(frame, frameProcessors):

    frameCoords = {}
    
    frameCoords["cylindersYellow"] = frameProcessors["cylindersYellow"].process(frame)[0]
    frameCoords["cylindersGreen"] = frameProcessors["cylindersGreen"].process(frame)[0]
    frameCoords["tennisBall"] = frameProcessors["tennisBall"].process(frame)[0]
    frameCoords["robots"] = frameProcessors["robots"].process(frame)[0]

    return frameCoords


def getTableCoords(frameCoords, perspectiveTransformer):

    tableCoords = {}
    
    tableCoords["cylindersYellow"] = perspectiveTransformer.transform(frameCoords["cylindersYellow"])
    tableCoords["cylindersGreen"] = perspectiveTransformer.transform(frameCoords["cylindersGreen"])
    tableCoords["tennisBall"] = perspectiveTransformer.transform(frameCoords["tennisBall"])
    tableCoords["robots"] = perspectiveTransformer.transform(frameCoords["robots"])

    return tableCoords
