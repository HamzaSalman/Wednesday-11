# Created by: Hamza Salman
# Created on: November 2016
# Created for: ICS3U
# this is the main scene.

from scene import *
import ui

from splash_scene import *


#  ..use when deploying app for Xcode and the App Store
main_view = ui.View()
scene_view = SceneView(frame = main_view.bounds, flex = 'WH')
main_view.add_subview(scene_view)
scene_view.scene = SplashScene()
main_view.present(hide_title_bar = True, animated = False)
