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
    gpxTrack.segments.append(gpxSegment)

    for record in fitfile.get_messages("record"):
        gpxTrackPoint = gpxpy.gpx.GPXTrackPoint()

        for data in record.fields:
            if data.name == "position_long":
                gpxTrackPoint.longitude = semicircles_to_degrees(data.value)
            if data.name == "position_lat":
                gpxTrackPoint.latitude  = semicircles_to_degrees(data.value)
            if data.name == "timestamp":
                gpxTrackPoint.time      = data.value
            if data.name == "altitude":
                gpxTrackPoint.elevation = round(data.value, 8)

        if not (gpxTrackPoint.latitude and gpxTrackPoint.longitude):
            continue

        gpxSegment.points.append(gpxTrackPoint)

    return gpx

