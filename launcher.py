from pract2d.game import gamemanager
from pract2d.core import files
from platform import system
import os

if __name__ == '__main__':
    try:
        if system() == 'Windows' or not os.environ["PYSDL2_DLL_PATH"]:
            os.environ["PYSDL2_DLL_PATH"] = files.get_path()
    except KeyError:
        pass
    game = gamemanager.GameManager()
    game.run()
