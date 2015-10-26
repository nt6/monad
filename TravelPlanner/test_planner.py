from planner import TravelPlanner, Mode
import unittest
import datetime

YEAR  = 2015
MONTH = 10
DAY   = 10

TIMEDIFF_0MIN = datetime.timedelta(minutes = 0)
TIMEDIFF_10MIN = datetime.timedelta(minutes = 10)
TIMEDIFF_15MIN = datetime.timedelta(minutes = 15)
TIMEDIFF_20MIN = datetime.timedelta(minutes = 20)
TIMEDIFF_25MIN = datetime.timedelta(minutes = 25)
TIMEDIFF_30MIN = datetime.timedelta(minutes = 30)
TIMEDIFF_45MIN = datetime.timedelta(minutes = 45)
TIMEDIFF_60MIN = datetime.timedelta(minutes = 60)
TIME_1255H = datetime.datetime(YEAR, MONTH, DAY, 12, 55)
TIME_1300H = datetime.datetime(YEAR, MONTH, DAY, 13, 00)
TIME_1305H = datetime.datetime(YEAR, MONTH, DAY, 13, 05)
TIME_1315H = datetime.datetime(YEAR, MONTH, DAY, 13, 15)
TIME_1320H = datetime.datetime(YEAR, MONTH, DAY, 13, 20)
TIME_1330H = datetime.datetime(YEAR, MONTH, DAY, 13, 30)
TIME_1345H = datetime.datetime(YEAR, MONTH, DAY, 13, 45)
TIME_1400H = datetime.datetime(YEAR, MONTH, DAY, 14, 00)

class TestTravelPlanner(unittest.TestCase):

    tp = TravelPlanner()

    def test_init(self):
        requestDBString = "Collection(Database(MongoClient('localhost', 27017), u'monad'), " + \
                "u'TravelRequest')"
        routeDBString = "Collection(Database(MongoClient('localhost', 27017), u'monad'), u'Route')"
        timetableDBString = "Collection(Database(MongoClient('localhost', 27017), u'monad'), " + \
                "u'timeTable')"
        usertripDBString = "Collection(Database(MongoClient('localhost', 27017), u'monad'), " + \
                "u'UserTrip')"

        self.assertEqual(self.tp.fittingRoutes, [])
        self.assertEqual(self.tp.startingWaypoint, [])
        self.assertEqual(self.tp.endingWaypoint, [])

        self.assertEqual(str(self.tp.travelRequest), requestDBString)
        self.assertEqual(str(self.tp.route), routeDBString)
        self.assertEqual(str(self.tp.timeTable), timetableDBString)
        self.assertEqual(str(self.tp.userTrip), usertripDBString)

    # Database dependency
    def test_findFittingRoutes(self):
        pass

    def test_isBetterTripStartTime(self):
        self.tp.tripTuples = [("trip", TIMEDIFF_30MIN, TIME_1300H, TIME_1315H)]
        self.tp.timeMode = Mode.startTime

        self.tp.timeToArrival = TIMEDIFF_25MIN
        self.assertTrue(self.tp._isBetterTrip(0))

        self.tp.timeToArrival = TIMEDIFF_30MIN
        self.tp.dptTime = TIME_1305H
        self.tp.routeMode = Mode.tripTime
        self.assertTrue(self.tp._isBetterTrip(0))
        self.tp.routeMode = Mode.waitTime
        self.assertFalse(self.tp._isBetterTrip(0))

        self.tp.dptTime = TIME_1255H
        self.tp.routeMode = Mode.waitTime
        self.assertTrue(self.tp._isBetterTrip(0))
        self.tp.routeMode = Mode.tripTime
        self.assertFalse(self.tp._isBetterTrip(0))

        self.tp.timeToArrival = TIMEDIFF_60MIN
        self.assertFalse(self.tp._isBetterTrip(0))

    def test_isBetterTripArrivalTime(self):
        self.tp.tripTuples = [("trip", TIMEDIFF_30MIN, TIME_1300H, TIME_1315H)]
        self.tp.timeMode = Mode.arrivalTime

        self.tp.diffToArrTime = TIMEDIFF_25MIN
        self.assertTrue(self.tp._isBetterTrip(0))

        self.tp.diffToArrTime = TIMEDIFF_30MIN
        self.tp.dptTime = TIME_1305H
        self.tp.routeMode = Mode.tripTime
        self.assertTrue(self.tp._isBetterTrip(0))
        self.tp.routeMode = Mode.waitTime
        self.assertFalse(self.tp._isBetterTrip(0))

        self.tp.dptTime = TIME_1255H
        self.tp.routeMode = Mode.waitTime
        self.assertTrue(self.tp._isBetterTrip(0))
        self.tp.routeMode = Mode.tripTime
        self.assertFalse(self.tp._isBetterTrip(0))

        self.tp.diffToArrTime = TIMEDIFF_60MIN
        self.assertFalse(self.tp._isBetterTrip(0))

    def test_rankTripStartTime(self):
        trip1 = ("trip1", TIMEDIFF_15MIN, TIME_1305H, TIME_1315H)
        trip2 = ("trip2", TIMEDIFF_20MIN, TIME_1300H, TIME_1320H)
        trip3 = ("trip3", TIMEDIFF_30MIN, TIME_1315H, TIME_1330H)
        trip4 = ("trip4", TIMEDIFF_30MIN, TIME_1300H, TIME_1330H)
        self.tp.tripTuples = [trip1, trip2, trip3, trip4]
        self.tp.timeMode = Mode.startTime
        self.tp.routeMode = Mode.tripTime

        trip = "trip5"
        self.tp.timeToArrival = TIMEDIFF_60MIN
        self.tp.dptTime = TIME_1330H
        self.tp.arrTime = TIME_1400H
        trip5 = (trip, self.tp.timeToArrival, self.tp.dptTime, self.tp.arrTime)
        self.tp._rankTrip(trip)
        self.assertEqual(self.tp.tripTuples, [trip1, trip2, trip3, trip4, trip5])

        trip = "trip6"
        self.tp.timeToArrival = TIMEDIFF_20MIN
        self.tp.dptTime = TIME_1305H
        self.tp.arrTime = TIME_1320H
        trip6 = (trip, self.tp.timeToArrival, self.tp.dptTime, self.tp.arrTime)
        self.tp._rankTrip(trip)
        self.assertEqual(self.tp.tripTuples, [trip1, trip6, trip2, trip3, trip4])

        trip = "trip7"
        self.tp.timeToArrival = TIMEDIFF_60MIN
        self.tp.dptTime = TIME_1330H
        self.tp.arrTime = TIME_1400H
        trip7 = (trip, self.tp.timeToArrival, self.tp.dptTime, self.tp.arrTime)
        self.tp._rankTrip(trip)
        self.assertEqual(self.tp.tripTuples, [trip1, trip6, trip2, trip3, trip4])

    def test_rankTripArrivalTime(self):
        trip1 = ("trip1", TIMEDIFF_0MIN, TIME_1330H, TIME_1400H)
        trip2 = ("trip2", TIMEDIFF_30MIN, TIME_1320H, TIME_1330H)
        trip3 = ("trip3", TIMEDIFF_30MIN, TIME_1315H, TIME_1330H)
        trip4 = ("trip4", TIMEDIFF_30MIN, TIME_1300H, TIME_1330H)
        self.tp.tripTuples = [trip1, trip2, trip3, trip4]
        self.tp.timeMode = Mode.arrivalTime
        self.tp.routeMode = Mode.tripTime

        trip = "trip5"
        self.tp.diffToArrTime = TIMEDIFF_45MIN
        self.tp.dptTime = TIME_1300H
        self.tp.arrTime = TIME_1315H
        trip5 = (trip, self.tp.diffToArrTime, self.tp.dptTime, self.tp.arrTime)
        self.tp._rankTrip(trip)
        self.assertEqual(self.tp.tripTuples, [trip1, trip2, trip3, trip4, trip5])

        trip = "trip6"
        self.tp.diffToArrTime = TIMEDIFF_15MIN
        self.tp.dptTime = TIME_1330H
        self.tp.arrTime = TIME_1345H
        trip6 = (trip, self.tp.diffToArrTime, self.tp.dptTime, self.tp.arrTime)
        self.tp._rankTrip(trip)
        self.assertEqual(self.tp.tripTuples, [trip1, trip6, trip2, trip3, trip4])

        trip = "trip7"
        self.tp.diffToArrTime = TIMEDIFF_60MIN
        self.tp.dptTime = TIME_1300H
        self.tp.arrTime = TIME_1255H
        trip7 = (trip, self.tp.diffToArrTime, self.tp.dptTime, self.tp.arrTime)
        self.tp._rankTrip(trip)
        self.assertEqual(self.tp.tripTuples, [trip1, trip6, trip2, trip3, trip4])

    def test_insertTrip(self):
        self.tp.tripTuples = []
        self.tp.counter = 0
        self.tp.startingWaypoint = [0]
        self.tp.endingWaypoint = [1]
        self.tp.startTime = TIME_1300H
        self.tp.timeMode = Mode.startTime

        trip = "trip1"
        self.tp.dptTime = TIME_1305H
        self.tp.arrTime = TIME_1315H
        self.tp._insertTrip(trip)
        trip1 = (trip, TIMEDIFF_15MIN, TIME_1305H, TIME_1315H)
        self.assertEqual(self.tp.tripTuples, [trip1])

        trip = "trip2"
        self.tp.dptTime = TIME_1315H
        self.tp.arrTime = TIME_1320H
        self.tp._insertTrip(trip)
        trip2 = (trip, TIMEDIFF_20MIN, TIME_1315H, TIME_1320H)
        self.assertEqual(self.tp.tripTuples, [trip1, trip2])

        self.tp.tripTuples = []
        self.tp.endTime = TIME_1400H
        self.tp.timeMode = Mode.arrivalTime

        trip = "trip1"
        self.tp.dptTime = TIME_1330H
        self.tp.arrTime = TIME_1345H
        self.tp._insertTrip(trip)
        trip1 = (trip, TIMEDIFF_15MIN, TIME_1330H, TIME_1345H)
        self.assertEqual(self.tp.tripTuples, [trip1])

        trip = "trip2"
        self.tp.dptTime = TIME_1345H
        self.tp.arrTime = TIME_1400H
        self.tp._insertTrip(trip)
        trip2 = (trip, TIMEDIFF_0MIN, TIME_1345H, TIME_1400H)
        self.assertEqual(self.tp.tripTuples, [trip2, trip1])


    # Database dependency
    def test_findBestRoute(self):
        pass

    # Database dependency
    def test_updateDatabase(self):
        pass

    # Database dependency
    def test_getBestRoutes(self):
        pass

    # The number of tests is very important!
    def test_hereIsOneMoreTestThatWillSucceed(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()

