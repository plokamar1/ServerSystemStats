import platform
import client

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
        print(package + ' was installed!')
    finally:
        globals()[package] = importlib.import_module(package)

if __name__ == "__main__":
    #install and import missing external libraries
    install_and_import('psutil')
    install_and_import('socket')
    install_and_import('configparser')
    if platform.system() == 'Linux':
        install_and_import('daemon')
        with daemon.DaemonContext():
            client.main()
    elif platform.system() == 'Windows':
        client.main()

