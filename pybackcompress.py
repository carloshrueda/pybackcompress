#! python
# -*- coding: utf-8 -*-

import argparse
from os import listdir, remove
from os.path import isfile, join, isdir


def compressfolders(hfolders, args):
    # TODO compressfolders
    pass


def compressfiles(harchivos, args):
    #colocar los archivos en un archivo temporal
    tmpfile= "./archivos.tmp"
    farch= open(tmpfile, "w")
    farch.writelines("\n".join(harchivos))
    farch.flush()
    farch.close()

    #armar comando 7zip
    # 7z.exe u -tzip -r "F:\Backup manual\Back_Programa.zip" "D:\Programa\" -mx9 -mmt=3 -xr@"D:\backups\PROCESOS\excluidos.txt" >> %FILELOG%
    cmd= '7z.exe %s %s -r %s %s %s -mmt=%s -xi@%s -xr@%s" >> %s"'
    # TODO ejarmar comando 7zip

    #ejecutar comando 7zip
    # TODO ejecutar comando 7zip

    #borrar archivo temporal
    if isfile(tmpfile):
        remove(tmpfile)
        pass


def main(args):
    # obtener archivos y folders
    harchivos = []
    hfolders = []
    path = args.o
    for item in listdir(path):
        ruta = join(path, item)
        harchivos.append(ruta) if isfile(ruta) else hfolders.append(ruta)

    #crear archivo log
    if args.l == "on":
        # TODO crear archivo log
        pass

    # comprimir archivos
    compressfiles(harchivos, args)

    # comprimir folders
    compressfolders(hfolders, args)


def getargumentos():
    parser = argparse.ArgumentParser(description='Haciendo backup con compresión', usage="%(prog)s [opciones]",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("o", help="ruta de origen")
    parser.add_argument("d", help="ruta de destino")

    parser.add_argument("-a", choices=['on', 'off'], help="actualizar archivos (por de defecto: %(default)s)",
                        default="on")
    parser.add_argument("-e", type=str, help="ruta del archivo con extensiones para excluir")
    parser.add_argument("-l", type=str, choices=['on', 'off'], help="log (por de defecto: %(default)s)", default="on")
    parser.add_argument("-nc", type=int, choices="09", help="nivel de compresion (por de defecto: %(default)s)",
                        default=9)
    parser.add_argument("-nh", type=int, help="número de hilos (por de defecto: %(default)s)", default=1)
    parser.add_argument("-t", type=str, choices=['7z', 'bzip2', 'zip'],
                        help="tipo de compresion (por de defecto: %(default)s)", default="zip")
    parser.add_argument("-dl", type=str, help="ruta destino log (por de defecto: %(default)s)", default=".")
    parser.add_argument("--verbose", help="mostrar información de depuración", default=argparse.SUPPRESS)
    parser.add_argument('-v', action='version', version='%(prog)s - Version 0.1', help="versión del programa",
                        default=argparse.SUPPRESS)
    args = parser.parse_args()

    # valildar rutas de origen
    if not isdir(args.o):
        print("Error. La ruta de ORIGEN: " + args.o + " no existe.")
        ha = None
        return

    if not isdir(args.d):
        print("Error. La ruta de DESTINO: " + args.d + " no existe.")
        ha = None
        return

    if args.l and not isdir(args.dl):
        print("Error. La ruta del LOG: " + args.dl + " no existe.")
        ha = None
        return

    if args.e is not None and not isdir(args.e):
        print("Error. La ruta del archivo para EXCLUIR: " + args.e + " no existe.")
        ha = None
        return

    return args


if __name__ == "__main__":
    args = None
    args = getargumentos()
    if args:
        main(args)
