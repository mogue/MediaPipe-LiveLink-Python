try:
    import pyi_splash

    # Update the text on the splash screen
    pyi_splash.update_text("WebCam Live Link!")
    pyi_splash.update_text("PauseChamp")

    pyi_splash.close()
except ImportError:
    pass

import data
import src