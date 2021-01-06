#!/usr/bin/python3

import gpxpy
import fitparse

def semicircles_to_degrees(sc) -> float:
    degrees = sc * (180/2**31)
    return round(degrees, 8)

def parse_fit_to_gpx(fitname) -> gpxpy.gpx.GPX:
    fitfile = fitparse.FitFile(fitname)

    gpx = gpxpy.gpx.GPX()

    gpxTrack = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpxTrack)

    gpxSegment = gpxpy.gpx.GPXTrackSegment()
    #gpxTrack.segments.append(gpxSegment)

    for message in fitfile.messages:
        if message.name == "lap":
            gpxTrack.segments.append(gpxSegment) # append the current TrackSegment to the GPX
            gpxSegment = gpxpy.gpx.GPXTrackSegment() # and start a new one for the records to follow
            # TODO: What happens if there is no 'lap' message at the end of the .fit file?

        if message.name == "record":
            gpxTrackPoint = gpxpy.gpx.GPXTrackPoint()

            for data in message.fields:
                if data.name == "position_long" and data.value != None:
                    gpxTrackPoint.longitude = semicircles_to_degrees(data.value)

                if data.name == "position_lat" and data.value != None:
                    gpxTrackPoint.latitude  = semicircles_to_degrees(data.value)
                
                if data.name == "timestamp":
                    gpxTrackPoint.time      = data.value
                
                if data.name == "altitude":
                    gpxTrackPoint.elevation = round(data.value, 8)

            if not (gpxTrackPoint.latitude and gpxTrackPoint.longitude):
                continue

            gpxSegment.points.append(gpxTrackPoint)

    return gpx

