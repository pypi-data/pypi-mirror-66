import os
from pathlib import Path

from aiohttp import web, MultipartWriter, MultipartReader

from plom import specdir
from .routeutils import authByToken, authByToken_validFields
from .routeutils import log

# I couldn't make this work with the auth deco
# routes = web.RouteTableDef()


class IDHandler:
    def __init__(self, plomServer):
        self.server = plomServer
        # self.local_route_table = routes

    # @routes.get("/ID/progress")
    @authByToken
    def IDprogressCount(self):
        return web.json_response(self.server.IDprogressCount(), status=200)

    # @routes.get("/ID/classlist")
    @authByToken
    def IDgetClasslist(self):
        if os.path.isfile(Path(specdir) / "classlist.csv"):
            return web.FileResponse(Path(specdir) / "classlist.csv", status=200)
        else:
            return web.Response(status=404)

    # @routes.get("/ID/predictions")
    @authByToken
    def IDgetPredictions(self):
        if os.path.isfile(Path(specdir) / "predictionlist.csv"):
            return web.FileResponse(Path(specdir) / "predictionlist.csv", status=200)
        else:
            return web.Response(status=404)

    # @routes.get("/ID/tasks/complete")
    @authByToken_validFields(["user"])
    def IDgetDoneTasks(self, data, request):
        # return the completed list
        return web.json_response(self.server.IDgetDoneTasks(data["user"]), status=200)

    # @routes.get("/ID/images/{test}")
    @authByToken_validFields(["user"])
    def IDgetImage(self, data, request):
        test = request.match_info["test"]
        rmsg = self.server.IDgetImage(data["user"], test)
        if not rmsg[0]:  # user allowed access - returns [true, fname0, fname1,...]
            return web.Response(status=409)  # someone else has that image
        with MultipartWriter("images") as mpwriter:
            for fn in rmsg[1:]:
                if os.path.isfile(fn):
                    mpwriter.append(open(fn, "rb"))
                else:
                    return web.Response(status=404)
            return web.Response(body=mpwriter, status=200)

    # @routes.get("/ID/tasks/available")
    @authByToken
    def IDgetNextTask(self):
        rmsg = self.server.IDgetNextTask()  # returns [True, code] or [False]
        if rmsg[0]:
            return web.json_response(rmsg[1], status=200)
        else:
            return web.Response(status=204)  # no papers left

    # @routes.patch("/ID/tasks/{task}")
    @authByToken_validFields(["user"])
    def IDclaimThisTask(self, data, request):
        testNumber = request.match_info["task"]
        rmsg = self.server.IDclaimThisTask(data["user"], testNumber)
        if rmsg[0]:  # user allowed access - returns [true, fname0, fname1,...]
            with MultipartWriter("images") as mpwriter:
                for fn in rmsg[1:]:
                    if os.path.isfile(fn):
                        mpwriter.append(open(fn, "rb"))
                    else:
                        return web.Response(status=404)
                return web.Response(body=mpwriter, status=200)
        else:
            return web.Response(status=204)  # that task already taken.

    # @routes.put("/ID/tasks/{task}")
    @authByToken_validFields(["user", "sid", "sname"])
    def IDreturnIDdTask(self, data, request):
        testNumber = request.match_info["task"]
        rmsg = self.server.IDreturnIDdTask(
            data["user"], testNumber, data["sid"], data["sname"]
        )
        # returns [True] if all good
        # [False, True] - if student number already in use
        # [False, False] - if bigger error
        if rmsg[0]:  # all good
            return web.Response(status=200)
        elif rmsg[1]:  # student number already in use
            return web.Response(status=409)
        else:  # a more serious error - can't find this in database
            return web.Response(status=404)

    # @routes.delete("/ID/tasks/{task}")
    @authByToken_validFields(["user"])
    def IDdidNotFinishTask(self, data, request):
        testNumber = request.match_info["task"]
        self.server.IDdidNotFinish(data["user"], testNumber)
        return web.json_response(status=200)

    # @routes.get("/ID/randomImage")
    @authByToken_validFields(["user"])
    def IDgetRandomImage(self, data, request):
        # TODO: maybe we want some special message here?
        if data["user"] != "manager":
            return web.Response(status=401)  # only manager

        rmsg = self.server.IDgetRandomImage()
        log.debug("Appending file {}".format(rmsg))
        with MultipartWriter("images") as mpwriter:
            for fn in rmsg[1:]:
                if os.path.isfile(fn):
                    mpwriter.append(open(fn, "rb"))
                else:
                    return web.Response(status=404)
            return web.Response(body=mpwriter, status=200)

    @authByToken_validFields(["user"])
    def IDdeletePredictions(self, data, request):
        # TODO: maybe we want some special message here?
        if data["user"] != "manager":
            return web.Response(status=401)

        return web.json_response(self.server.IDdeletePredictions(), status=200)

    @authByToken_validFields(["user", "rectangle", "fileNumber", "ignoreStamp"])
    def IDrunPredictions(self, data, request):
        # TODO: maybe we want some special message here?
        if data["user"] != "manager":
            return web.Response(status=401)

        rmsg = self.server.IDrunPredictions(
            data["rectangle"], data["fileNumber"], data["ignoreStamp"]
        )
        if rmsg[0]:  # set running or is running
            if rmsg[1]:
                return web.Response(status=200)
            else:
                return web.Response(status=202)  # is already running
        else:  # isn't running because we found a time-stamp
            return web.Response(text=rmsg[1], status=205)

    # @routes.patch("/ID/review")
    @authByToken_validFields(["testNumber"])
    def IDreviewID(self, data, request):
        if self.server.IDreviewID(data["testNumber"]):
            return web.Response(status=200)
        else:
            return web.Response(status=404)

    def setUpRoutes(self, router):
        # router.add_routes(self.local_route_table)
        # But see above: doesn't work with auth deco
        router.add_get("/ID/progress", self.IDprogressCount)
        router.add_get("/ID/classlist", self.IDgetClasslist)
        router.add_get("/ID/predictions", self.IDgetPredictions)
        router.add_get("/ID/tasks/complete", self.IDgetDoneTasks)
        router.add_get("/ID/images/{test}", self.IDgetImage)
        router.add_get("/ID/tasks/available", self.IDgetNextTask)
        router.add_patch("/ID/tasks/{task}", self.IDclaimThisTask)
        router.add_put("/ID/tasks/{task}", self.IDreturnIDdTask)
        router.add_delete("/ID/tasks/{task}", self.IDdidNotFinishTask)
        router.add_get("/ID/randomImage", self.IDgetRandomImage)
        router.add_delete("/ID/predictedID", self.IDdeletePredictions)
        router.add_post("/ID/predictedID", self.IDrunPredictions)
        router.add_patch("/ID/review", self.IDreviewID)
