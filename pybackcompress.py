#! python
# -*- coding: utf-8 -*-

import argparse
import os


def main(args):
    # Aquí procesamos lo que se tiene que hacer con cada argumento
    print("Argumento: ", args)


def getargumentos(ha):
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
    ha = parser.parse_args()

    # valildar rutas de origen
    if not os.path.isdir(ha.o):
        print("Error. La ruta de ORIGEN: " + ha.o + " no existe.")
        ha = None
        return

    if not os.path.isdir(ha.d):
        print("Error. La ruta de DESTINO: " + ha.d + " no existe.")
        ha = None
        return

    if ha.l and not os.path.isdir(ha.dl):
        print("Error. La ruta del LOG: " + ha.dl + " no existe.")
        ha = None
        return

    if ha.e is not None and not os.path.isdir(ha.e):
        print("Error. La ruta del archivo para EXCLUIR: " + ha.e + " no existe.")
        ha = None
        return


if __name__ == "__main__":
    hargs = None
    getargumentos(hargs)
    if hargs:
        main(hargs)
