#! python
# -*- coding: utf-8 -*-

import argparse
from os import listdir, remove, getcwd, chdir, system
from os.path import isfile, join, isdir, dirname, abspath
from time import strftime
import sys
import subprocess


def logwritehdl(hdl, msg):
    hdl.write("[" + strftime("%Y%m%d@%H:%M:%S") + "] " + msg + "\n")
    hdl.flush()


def logwrite(logpath, msg):
    logfile = open(logpath, "a")
    logfile.write("[" + strftime("%Y%m%d@%H:%M:%S") + "] " + msg + "\n")
    logfile.flush()
    logfile.close()


def printverbose(verbose, msg, msg2=""):
    if verbose == "on":
        print("[" + strftime("%Y%m%d@%H:%M:%S") + "] [%s] %s" % (msg, msg2))
        sys.stdout.flush()


def compressfolders(hfolders, args, exclufiles, logfile):
    logwrite(logfile, "[START COMPRESSFOLDER] ")
    printverbose(args.verbose, "START COMPRESSFOLDER")
    progpath = dirname(abspath(__file__)).replace("\\", "/") + "/"

    # cambio de directorio de trabajo
    workdir = args.wd.replace("\\", "/")
    chdir(workdir)

    # RECORRER LOS DIRECTORIOS
    dest = args.d.replace("\\", "/")
    ext = args.t
    if args.t == "bzip":
        ext = "bz"
    for folder in hfolders:
        logwrite(logfile, "[INIT FOLDER] " + folder)
        printverbose(args.verbose, "INIT FOLDER", folder)

        # armar comando 7zip
        # 7z.exe u -tzip -r "F:\Backup manual\Back_Programa.zip" -mx9 -mmt=3 -ir@"D:\backups\PROCESOS\includos" -xr@"D:\backups\PROCESOS\excluidos" >> %FILELOG%
        # cmd = '7za.exe %s %s -r %s %s %s -mmt=%s -xi@%s -xr@%s" >> %s"'
        cmd = '"%s7za.exe" ' % (progpath)
        cmd += "u " if args.a == "on" else "a "  # actualizar
        cmd += "-t%s " % (args.t)  # metodo de compresion

        # destino
        orig = folder.replace("\\", "/")
        ultorig = orig.split("/")
        cmd += '"%s/%s.%s" ' % (dest, ultorig[-1], ext)

        # origen
        cmd += '"%s" ' % (orig)

        # excluidos
        if exclufiles:
            exclufiles = exclufiles.replace('\\', "/")
            cmd += '-xr@"%s" ' % (exclufiles) if exclufiles else ""

        # nivel de compresion
        cmd += "-mx%d " % (args.nc)
        # hilos
        cmd += "-mmt=%d " % (args.nh)
        # directorio de trabajo
        cmd += '-w"%s" ' % (workdir)
        # logfile
        cmd += '-scsWIN >> "%s"' % (logfile)

        # agregar comando al logfile
        logwrite(logfile, "[CMD] " + cmd)
        printverbose(args.verbose, "CMD ", cmd)

        # ejecutar comando 7zip
        cmdexec = subprocess.call(cmd, shell=True)
        logwrite(logfile, "[CMDOUT] " + str(cmdexec))
        printverbose(args.verbose, "CMDOUT", str(cmdexec))

        logwrite(logfile, "[FINISH FOLDER] " + folder)
        printverbose(args.verbose, "FINISH FOLDER", folder)

    logwrite(logfile, "[END COMPRESSFOLDER] ")
    printverbose(args.verbose, "END COMPRESSFOLDER")


def compressfiles(harchivos, args, exclufiles, logfile):
    # colocar los archivos en un archivo temporal
    logwrite(logfile, "[START COMPRESSFILE]")
    printverbose(args.verbose, "START COMPRESSFILE")

    # cambio de directorio de trabajo
    workdir = args.wd.replace("\\", "/")
    chdir(workdir)

    # archivo temporal de los incluidos
    progpath = dirname(abspath(__file__)).replace("\\", "/") + "/"
    tmpfile = progpath + "incluidos.tmp"
    printverbose(args.verbose, "INCLUDE FILE", tmpfile)
    farch = open(tmpfile, "w")
    strfiles = "\n".join(harchivos)
    farch.writelines(strfiles)
    farch.flush()
    farch.close()

    logwrite(logfile, "[START FILES] \n%s" % (strfiles))
    printverbose(args.verbose, "START FILES", "\n%s" % (strfiles))
    logwrite(logfile, "[END FILES]")
    printverbose(args.verbose, "END FILES")

    # armar comando 7zip
    # 7z.exe u -tzip -r "F:\Backup manual\Back_Programa.zip" -mx9 -mmt=3 -ir@"D:\backups\PROCESOS\includos" -xr@"D:\backups\PROCESOS\excluidos" >> %FILELOG%
    # cmd = '7za.exe %s %s -r %s %s %s -mmt=%s -xi@%s -xr@%s" >> %s"'
    cmd = '"%s7za.exe" ' % (progpath)
    cmd += "u " if args.a == "on" else "a "  # actualizar
    cmd += "-t%s " % (args.t)  # metodo de compresion

    # destino
    dest = args.d.replace("\\", "/")
    orig = args.o.replace("\\", "/")
    ultorig = orig.split("/")
    ext = args.t
    if args.t == "bzip":
        ext = "bz"
    cmd += '"%s/%s.%s" ' % (dest, ultorig[-1], ext)

    # origen
    # cmd += '"%s/*.*" ' % (org)

    # incluidos
    cmd += '@"%s" ' % (tmpfile)

    # excluidos
    if exclufiles:
        exclufiles = exclufiles.replace('\\', "/")
        cmd += '-xr@"%s" ' % (exclufiles) if exclufiles else ""

    # nivel de compresion
    cmd += "-mx%d " % (args.nc)
    # hilos
    cmd += "-mmt=%d " % (args.nh)
    # directorio de trabajo
    cmd += '-w"%s" ' % (workdir)
    # logfile
    cmd += '-scsWIN >> "%s"' % (logfile)

    # agregar comando al logfile
    logwrite(logfile, "[CMD] " + cmd)
    printverbose(args.verbose, "CMD ", cmd)

    # ejecutar comando 7zip
    cmdexec = subprocess.call(cmd, shell=True)
    logwrite(logfile, "[CMDOUT] " + str(cmdexec))
    printverbose(args.verbose, "CMDOUT", str(cmdexec))

    # borrar archivo temporal
    if isfile(tmpfile):
        remove(tmpfile)

    logwrite(logfile, "[END COMPRESSFILE] ")
    printverbose(args.verbose, "END COMPRESSFILE")


def main(args):
    # obtener archivos y folders
    harchivos = []
    hfolders = []
    path = args.o
    for item in listdir(path):
        ruta = join(path, item)
        harchivos.append(ruta) if isfile(ruta) else hfolders.append(ruta)

    # crear archivo log
    if args.l == "on":
        logpath = args.dl.replace("\\", "/")
        logpath = logpath + "/" + strftime("%Y%m%d") + "-" + args.nl

    printverbose(args.verbose, "PROCESS START")
    logwrite(logpath, "[" + strftime("%Y%m%d@%H:%M:%S") + "] [PROCESS START]") if args.l == "on" else None

    printverbose(args.verbose, "LOG FILE", logpath)


    # comprimir archivos
    compressfiles(harchivos, args, args.e, logpath)

    # comprimir folders
    compressfolders(hfolders, args, args.e, logpath)


def getargumentos():
    parser = argparse.ArgumentParser(description='Haciendo backup con compresión', usage="%(prog)s [opciones]",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("o", help="directorio de origen")
    parser.add_argument("d", help="directorio de destino")

    parser.add_argument("-a", choices=['on', 'off'], help="actualizar archivos (por de defecto: %(default)s)",
                        default="on")
    parser.add_argument("-wd", type=str, help="Directorio de trabajo por de defecto: %(default)s)", default="./")
    parser.add_argument("-e", type=str, help="ruta y nombre del archivo con extensiones para excluir")
    parser.add_argument("-l", type=str, choices=['on', 'off'], help="log (por de defecto: %(default)s)", default="on")
    parser.add_argument("-nc", type=int, choices="09", help="nivel de compresion (por de defecto: %(default)s)",
                        default=9)
    parser.add_argument("-nh", type=int, help="número de hilos (por de defecto: %(default)s)", default=1)
    parser.add_argument("-t", type=str, choices=['7z', 'bzip2', 'zip'],
                        help="tipo de compresion (por de defecto: %(default)s)", default="zip")
    parser.add_argument("-dl", type=str, help="ruta del log (por de defecto: %(default)s)",
                        default="work directory")
    parser.add_argument("-nl", type=str, help="nombre archivo del log (por de defecto: %(default)s)",
                        default="pybackcompress.log")
    parser.add_argument("--verbose", choices=['on', 'off'],
                        help="mostrar información de depuración (por de defecto: %(default)s)", default="off")
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

    # print("args: ", args)
    # print("args.wd: ", args.wd )
    # sys.stdout.flush()
    if args.wd is '.':
        args.wd = args.d

    if not isdir(args.wd):
        print("Error. El DIRECTORIO DE TRABAJO: " + args.wd + " no existe.")
        ha = None
        return

    if args.l == "on":
        if args.dl == "work directory":
            args.dl = args.wd
        elif not isdir(args.dl):
            print("Error. La ruta del LOG: " + args.dl + " no existe.")
            ha = None
            return

        args.nl = args.nl.strip()
        if args.nl in [None, ""]:
            print("Error. El nombre del LOG: " + args.dl + " no es valido.")
            ha = None
            return

        args.log= "hola"

    if args.e and not isfile(args.e):
        print("Error. El archivo para EXCLUIR: " + args.e + " no existe.")
        ha = None
        return

    return args


## PROGRAMA PRINCIPAL
if __name__ == "__main__":
    args = None
    args = getargumentos()
    if args:
        main(args)
