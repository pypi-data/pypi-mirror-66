import os

# TODO: this script is handy for dev work but maybe we shouldn't ship it...
os.system("rm -rf collidingPages decodedPages discardedPages sentPages unknownPages pageImages")
os.system("rm -rf scannedExams/png")
# TODO: bit scary for a production system
#os.system("rm -rf archivedPDFs")
