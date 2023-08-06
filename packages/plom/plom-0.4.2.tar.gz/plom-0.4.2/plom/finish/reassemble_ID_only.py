# -*- coding: utf-8 -*-

__author__ = "Andrew Rechnitzer"
__copyright__ = "Copyright (C) 2020 Andrew Rechnitzer and Colin Macdonald"
__credits__ = ["Andrew Rechnitzer", "Colin Macdonald"]
__license__ = "AGPL-3.0-or-later"
# SPDX-License-Identifier: AGPL-3.0-or-later

import getpass
import os
import shlex
import subprocess
from multiprocessing import Pool
from tqdm import tqdm

from .testReassembler import reassemble
from plom.messenger import FinishMessenger
from plom.plom_exceptions import *
from plom.finish.locationSpecCheck import locationAndSpecCheck

numberOfTests = 0
numberOfQuestions = 0


# Parallel function used below, must be defined in root of module
def parfcn(y):
    reassemble(*y)


def reassembleTestCMD(msgr, shortName, outDir, t, sid):
    fnames = msgr.RgetOriginalFiles(t)
    if len(fnames) == 0:
        # TODO: what is supposed to happen here?
        return
    rnames = fnames
    outname = os.path.join(outDir, "{}_{}.pdf".format(shortName, sid))
    # reassemble(outname, shortName, sid, None, rnames)
    return (outname, shortName, sid, None, rnames)


def main(server=None, pwd=None):
    if server and ":" in server:
        s, p = server.split(":")
        msgr = FinishMessenger(s, port=p)
    else:
        msgr = FinishMessenger(server)
    msgr.start()

    if not pwd:
        pwd = getpass.getpass("Please enter the 'manager' password: ")

    try:
        msgr.requestAndSaveToken("manager", pwd)
    except PlomExistingLoginException:
        print(
            "You appear to be already logged in!\n\n"
            "  * Perhaps a previous session crashed?\n"
            "  * Do you have another finishing-script or manager-client running,\n"
            "    e.g., on another computer?\n\n"
            "In order to force-logout the existing authorisation run `plom-finish clear`."
        )
        exit(1)

    shortName = msgr.getInfoShortName()
    spec = msgr.getInfoGeneral()

    if not locationAndSpecCheck(spec):
        print("Problems confirming location and specification. Exiting.")
        msgr.closeUser()
        msgr.stop()
        exit(1)

    outDir = "reassembled_ID_but_not_marked"
    os.makedirs(outDir, exist_ok=True)

    identifiedTests = msgr.RgetIdentified()
    pagelists = []
    for t in identifiedTests:
        if identifiedTests[t][0] is not None:
            dat = reassembleTestCMD(msgr, shortName, outDir, t, identifiedTests[t][0])
            pagelists.append(dat)
        else:
            print(">>WARNING<< Test {} has no ID".format(t))

    msgr.closeUser()
    msgr.stop()

    N = len(pagelists)
    print("Reassembling {} papers...".format(N))
    with Pool() as p:
        r = list(tqdm(p.imap_unordered(parfcn, pagelists), total=N))

    print(">>> Warning <<<")
    print(
        "This still gets files by looking into server directory. In future this should be done over http."
    )


if __name__ == "__main__":
    main()
