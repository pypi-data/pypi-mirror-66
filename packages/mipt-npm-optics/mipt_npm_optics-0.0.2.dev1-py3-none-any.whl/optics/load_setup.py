import os
import pickle

import appdirs
import abc

class Setup(abc.ABC):
    @abc.abstractmethod
    def generate(self):
        pass

def load_setup(cls: Setup):
    name = str(cls.__name__) + ".pyobj"
    appname = "labs"
    author = "npm"
    path = appdirs.user_data_dir(appname, author)
    file_path = os.path.join(path, name)
    if os.path.exists(file_path):
        with open(file_path, "rb") as fin:
            setup = pickle.load(fin)
    else:
        os.makedirs(path, exist_ok=True)
        setup = cls.generate()
        with open(file_path, "wb") as fout:
            pickle.dump(setup,fout)
    return setup