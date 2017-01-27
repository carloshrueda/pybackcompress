# -*- coding: utf-8 -*-

import argparse


def main(args):
    # Aquí procesamos lo que se tiene que hacer con cada argumento
    if args.verbose:
        print("depuración activada!!!", args.verbose)

    if args.file:
        print("El nombre de archivo a procesar es: ", args.file)


def addArgumentos(p):
    p.add_argument("-d", help="Ruta de destino")
    p.add_argument("-ex", help="[-ex archivo] Archivo con extensiones para excluir")
    p.add_argument("-mt", help="[-h num] Numero de hilos")
    p.add_argument("-n", help="[-n nivel(0..9)] nivel de compresion")
    p.add_argument("-o", help="Ruta de origen")
    p.add_argument("-t", help="[-t tipo_compress (7z, zip, bzip2)] Tipo de compresion")
    p.add_argument("-u", help="[-u on | off] Actualizar")
    p.add_argument("-v", help="Mostrar información de depuración", action="store_true")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    addArgumentos(parser)
    args = parser.parse_args()

    main(args)
