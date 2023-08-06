from aiohttp import web, MultipartWriter, MultipartReader

from .routeutils import authByToken, authByToken_validFields
from .routeutils import validFields


class UploadHandler:
    def __init__(self, plomServer):
        self.server = plomServer

    async def uploadKnownPage(self, request):
        reader = MultipartReader.from_response(request)

        part0 = await reader.next()  # should be parameters
        if part0 is None:  # weird error
            return web.Response(status=406)  # should have sent 3 parts
        param = await part0.json()

        if not validFields(
            param, ["user", "token", "test", "page", "version", "fileName", "md5sum"]
        ):
            return web.Response(status=400)
        if not self.server.validate(param["user"], param["token"]):
            return web.Response(status=401)
        if not param["user"] in ("manager", "scanner"):
            return web.Response(status=401)

        # TODO: unused, we should ensure this matches the data
        # TODO: or why bother passing those in to param?
        code = request.match_info["tpv"]

        part1 = await reader.next()  # should be the image file
        if part1 is None:  # weird error
            return web.Response(status=406)  # should have sent 3 parts
        image = await part1.read()
        # file it away.
        rmsg = self.server.addKnownPage(
            param["test"],
            param["page"],
            param["version"],
            param["fileName"],
            image,
            param["md5sum"],
        )
        return web.json_response(rmsg, status=200)  # all good

    async def uploadUnknownPage(self, request):
        reader = MultipartReader.from_response(request)

        part0 = await reader.next()  # should be parameters
        if part0 is None:  # weird error
            return web.Response(status=406)  # should have sent 3 parts
        param = await part0.json()

        if not validFields(param, ["user", "token", "fileName", "md5sum"]):
            return web.Response(status=400)
        if not self.server.validate(param["user"], param["token"]):
            return web.Response(status=401)
        if not param["user"] in ("manager", "scanner"):
            return web.Response(status=401)

        part1 = await reader.next()  # should be the image file
        if part1 is None:  # weird error
            return web.Response(status=406)  # should have sent 3 parts
        image = await part1.read()
        # file it away.
        rmsg = self.server.addUnknownPage(param["fileName"], image, param["md5sum"],)
        return web.json_response(rmsg, status=200)  # all good

    async def uploadCollidingPage(self, request):
        reader = MultipartReader.from_response(request)

        part0 = await reader.next()  # should be parameters
        if part0 is None:  # weird error
            return web.Response(status=406)  # should have sent 2 parts
        param = await part0.json()

        if not validFields(
            param, ["user", "token", "fileName", "md5sum", "test", "page", "version"]
        ):
            return web.Response(status=400)
        if not self.server.validate(param["user"], param["token"]):
            return web.Response(status=401)
        if not param["user"] in ("manager", "scanner"):
            return web.Response(status=401)

        # TODO: unused, we should ensure this matches the data
        code = request.match_info["tpv"]

        part1 = await reader.next()  # should be the image file
        if part1 is None:  # weird error
            return web.Response(status=406)  # should have sent 2 parts
        image = await part1.read()
        # file it away.
        rmsg = self.server.addCollidingPage(
            param["test"],
            param["page"],
            param["version"],
            param["fileName"],
            image,
            param["md5sum"],
        )
        return web.json_response(rmsg, status=200)  # all good

    async def replaceMissingPage(self, request):
        data = await request.json()
        if not validFields(data, ["user", "token", "test", "page", "version"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        # TODO: unused, we should ensure this matches the data
        code = request.match_info["tpv"]

        rval = self.server.replaceMissingPage(
            data["test"], data["page"], data["version"]
        )
        if rval[0]:
            return web.json_response(rval, status=200)  # all fine
        else:
            return web.Response(status=404)  # page not found at all

    async def removeScannedPage(self, request):
        data = await request.json()
        if not validFields(data, ["user", "token", "test", "page", "version"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        # TODO: unused, we should ensure this matches the data
        code = request.match_info["tpv"]

        rval = self.server.removeScannedPage(
            data["test"], data["page"], data["version"]
        )
        if rval[0]:
            return web.json_response(rval, status=200)  # all fine
        else:
            return web.Response(status=404)  # page not found at all

    async def getUnknownPageNames(self, request):
        data = await request.json()
        if not validFields(data, ["user", "token"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.getUnknownPageNames()
        return web.json_response(rval, status=200)  # all fine

    async def getDiscardNames(self, request):
        data = await request.json()
        if not validFields(data, ["user", "token"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.getDiscardNames()
        return web.json_response(rval, status=200)  # all fine

    async def getCollidingPageNames(self, request):
        data = await request.json()
        if not validFields(data, ["user", "token"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.getCollidingPageNames()
        return web.json_response(rval, status=200)  # all fine

    async def getPageImage(self, request):
        data = await request.json()
        if not validFields(data, ["user", "token", "test", "page", "version"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        # TODO: unused, we should ensure this matches the data
        code = request.match_info["tpv"]

        rval = self.server.getPageImage(data["test"], data["page"], data["version"])
        if rval[0]:
            return web.FileResponse(rval[1], status=200)  # all fine
        else:
            return web.Response(status=404)

    async def getUnknownImage(self, request):
        data = await request.json()
        if not validFields(data, ["user", "token", "fileName"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.getUnknownImage(data["fileName"])
        if rval[0]:
            return web.FileResponse(rval[1], status=200)  # all fine
        else:
            return web.Response(status=404)

    async def getDiscardImage(self, request):
        data = await request.json()
        if not validFields(data, ["user", "token", "fileName"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.getDiscardImage(data["fileName"])
        if rval[0]:
            return web.FileResponse(rval[1], status=200)  # all fine
        else:
            return web.Response(status=404)

    async def getCollidingImage(self, request):
        data = await request.json()
        if not validFields(data, ["user", "token", "fileName"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.getCollidingImage(data["fileName"])
        if rval[0]:
            return web.FileResponse(rval[1], status=200)  # all fine
        else:
            return web.Response(status=404)

    # @route.get("/admin/questionImages")
    @authByToken_validFields(["user", "test", "question"])
    def getQuestionImages(self, data, request):
        if not data["user"] == "manager":
            return web.Response(status=401)

        rmsg = self.server.getQuestionImages(data["test"], data["question"])
        # returns either [True, fname1,fname2,..,fname.n] or [False, error]
        if rmsg[0]:
            with MultipartWriter("images") as mpwriter:
                for fn in rmsg[1:]:
                    mpwriter.append(open(fn, "rb"))
            return web.Response(body=mpwriter, status=200)
        else:
            return web.Response(status=404)  # couldnt find that test/question

    # @routes.get("/admin/testImages")
    @authByToken_validFields(["user", "test"])
    def getTestImages(self, data, request):
        if not data["user"] == "manager":
            return web.Response(status=401)

        rmsg = self.server.getTestImages(data["test"])
        # returns either [True, fname1,fname2,..,fname.n] or [False, error]
        if rmsg[0]:
            with MultipartWriter("images") as mpwriter:
                for fn in rmsg[1:]:
                    if fn is "":
                        mpwriter.append("")
                    else:
                        mpwriter.append(open(fn, "rb"))
            return web.Response(body=mpwriter, status=200)
        else:
            return web.Response(status=404)  # couldnt find that test/question

    async def checkPage(self, request):
        data = await request.json()
        if not validFields(data, ["user", "token", "test", "page", "images"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rmsg = self.server.checkPage(data["test"], data["page"])
        # returns either [True, version, fname], [True, version] or [False]
        if rmsg[0]:
            with MultipartWriter("images") as mpwriter:
                mpwriter.append("{}".format(rmsg[1]))
                if len(rmsg) == 3:
                    mpwriter.append(open(rmsg[2], "rb"))
            return web.Response(body=mpwriter, status=200)
        else:
            return web.Response(status=404)  # couldnt find that test/question

    async def removeUnknownImage(self, request):
        data = await request.json()
        if not validFields(data, ["user", "token", "fileName"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.removeUnknownImage(data["fileName"])
        if rval[0]:
            return web.Response(status=200)  # all fine
        else:
            return web.Response(status=404)

    async def removeCollidingImage(self, request):
        data = await request.json()
        if not validFields(data, ["user", "token", "fileName"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.removeCollidingImage(data["fileName"])
        if rval[0]:
            return web.Response(status=200)  # all fine
        else:
            return web.Response(status=404)

    async def unknownToTestPage(self, request):
        data = await request.json()
        if not validFields(
            data, ["user", "token", "fileName", "test", "page", "rotation"]
        ):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.unknownToTestPage(
            data["fileName"], data["test"], data["page"], data["rotation"]
        )
        if rval[0]:
            return web.json_response(rval[1], status=200)  # all fine
        else:
            return web.Response(status=404)

    async def unknownToExtraPage(self, request):
        data = await request.json()
        if not validFields(
            data, ["user", "token", "fileName", "test", "question", "rotation"]
        ):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.unknownToExtraPage(
            data["fileName"], data["test"], data["question"], data["rotation"]
        )
        if rval[0]:
            return web.Response(status=200)  # all fine
        else:
            return web.Response(status=404)

    async def collidingToTestPage(self, request):
        data = await request.json()
        if not validFields(
            data, ["user", "token", "fileName", "test", "page", "version"]
        ):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.collidingToTestPage(
            data["fileName"], data["test"], data["page"], data["version"]
        )
        if rval[0]:
            return web.Response(status=200)  # all fine
        else:
            return web.Response(status=404)

    async def discardToUnknown(self, request):
        data = await request.json()
        if not validFields(data, ["user", "token", "fileName"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.discardToUnknown(data["fileName"])
        if rval[0]:
            return web.Response(status=200)  # all fine
        else:
            return web.Response(status=404)

    def setUpRoutes(self, router):
        router.add_put("/admin/knownPages/{tpv}", self.uploadKnownPage)
        router.add_put("/admin/unknownPages", self.uploadUnknownPage)
        router.add_put("/admin/collidingPages/{tpv}", self.uploadCollidingPage)
        router.add_put("/admin/missingPage/{tpv}", self.replaceMissingPage)
        router.add_delete("/admin/scannedPage/{tpv}", self.removeScannedPage)
        router.add_get("/admin/scannedPage/{tpv}", self.getPageImage)
        router.add_get("/admin/unknownPageNames", self.getUnknownPageNames)
        router.add_get("/admin/discardNames", self.getDiscardNames)
        router.add_get("/admin/collidingPageNames", self.getCollidingPageNames)
        router.add_get("/admin/unknownImage", self.getUnknownImage)
        router.add_get("/admin/discardImage", self.getDiscardImage)
        router.add_get("/admin/collidingImage", self.getCollidingImage)
        router.add_get("/admin/questionImages", self.getQuestionImages)
        router.add_get("/admin/testImages", self.getTestImages)
        router.add_get("/admin/checkPage", self.checkPage)
        router.add_delete("/admin/unknownImage", self.removeUnknownImage)
        router.add_delete("/admin/collidingImage", self.removeCollidingImage)
        router.add_put("/admin/unknownToTestPage", self.unknownToTestPage)
        router.add_put("/admin/unknownToExtraPage", self.unknownToExtraPage)
        router.add_put("/admin/collidingToTestPage", self.collidingToTestPage)
        router.add_put("/admin/discardToUnknown", self.discardToUnknown)
